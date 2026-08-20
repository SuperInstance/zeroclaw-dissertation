#!/usr/bin/env python3
"""E3 field runner — elicited 7-dial readings from real model readers.

One independent API call per (reader, window, pass/paraphrase). Temperature 0.
Strict JSON validation with up to 2 repair attempts (the parse error is fed
back). Resume-safe: completed calls are cached and skipped on re-run.

Readers (registered roster; see REGISTRATION-2026-08-19.md):
  gateway (:8787)  -> glm-5.3, glm-5.2 (zai), deepseek-chat, deepseek-reasoner
  deepinfra direct -> Seed-2.0-mini/pro, Qwen3.6-35B-A3B, Hermes-3-405B,
                      claude-sonnet-5, gemma-4-31B-it, MiniMax-M3,
                      Nemotron-3-Super-120B-A12B, Qwen3.5-397B-A17B

Run:  bash -ic 'python3 elicit.py'   (deepinfra key comes from the shell env)
"""
import concurrent.futures as cf
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prompts import DIALS, SWEEP_WINDOWS, build_prompt  # noqa: E402

GATEWAY = "http://localhost:8787/v1/chat/completions"
DEEPINFRA = "https://api.deepinfra.com/v1/chat/completions"
KEY = os.environ.get("DEEPINFRA_API_KEY", "")

CORPUS = json.load(open(os.path.join(HERE, "corpus", "corpus.json")))
WINDOWS = {w["id"]: w for w in CORPUS["windows"]}

READERS = [
    # id,               endpoint,     model
    ("glm-5.3",         "gateway",    "glm-5.3"),
    ("glm-5.2",         "gateway",    "glm-5.2"),
    ("ds-v4-flash",     "gateway",    "deepseek-chat"),
    ("ds-v4-pro",       "gateway",    "deepseek-reasoner"),
    ("seed-2.0-mini",   "deepinfra",  "ByteDance/Seed-2.0-mini"),
    ("seed-2.0-pro",    "deepinfra",  "ByteDance/Seed-2.0-pro"),
    ("qwen3.6-35b",     "deepinfra",  "Qwen/Qwen3.6-35B-A3B"),
    ("qwen3.5-397b",    "deepinfra",  "Qwen/Qwen3.5-397B-A17B"),
    ("hermes-3-405b",   "deepinfra",  "NousResearch/Hermes-3-Llama-3.1-405B"),
    ("claude-sonnet-5", "deepinfra",  "anthropic/claude-sonnet-5"),
    ("gemma-4-31b",     "deepinfra",  "google/gemma-4-31B-it"),
    ("minimax-m3",      "deepinfra",  "MiniMaxAI/MiniMax-M3"),
    ("nemotron-120b",   "deepinfra",  "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B"),
]

MAX_TOKENS = 4000
TIMEOUT = 300
CONCURRENCY = int(os.environ.get("E3_CONCURRENCY", "24"))
RDIR = os.path.join(HERE, "readings", "raw")
SDIR = os.path.join(HERE, "sweep", "raw")


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def call(endpoint, model, messages, use_json_object=True, temperature=0):
    url = GATEWAY if endpoint == "gateway" else DEEPINFRA
    headers = {"Content-Type": "application/json"}
    if endpoint == "deepinfra":
        if not KEY:
            raise RuntimeError("DEEPINFRA_API_KEY missing (run under bash -ic)")
        headers["Authorization"] = f"Bearer {KEY}"
    body = {"model": model, "messages": messages,
            "max_tokens": MAX_TOKENS, "temperature": temperature}
    if use_json_object:
        body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(url, json.dumps(body).encode(),
                                 headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
        content = data["choices"][0]["message"].get("content") or ""
        usage = data.get("usage", {})
        return content, usage, time.time() - t0
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")[:300]
        raise RuntimeError(f"HTTP {e.code}: {err}") from e
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError,
            KeyError, IndexError) as e:
        raise RuntimeError(f"NET: {type(e).__name__}: {e}") from e


def call_with_retries(endpoint, model, messages, n_net=4):
    """Network-level retries (429/5xx/timeout) + json_object capability fallback.
    Returns (content, meta)."""
    use_json_object, last = True, None
    for attempt in range(n_net):
        try:
            content, usage, dt = call(endpoint, model, messages, use_json_object)
            return content, {"usage": usage, "dt": dt, "json_object": use_json_object}
        except RuntimeError as e:
            last = e
            s = str(e)
            if "400" in s and ("response_format" in s or "json_object" in s
                               or "json mode" in s.lower()) and use_json_object:
                use_json_object = False
                continue
            if "400" in s and "temperature" in s:
                # provider rejects temperature=0; retry with 0.01
                try:
                    content, usage, dt = call(endpoint, model, messages,
                                              use_json_object, temperature=0.01)
                    return content, {"usage": usage, "dt": dt,
                                     "json_object": use_json_object,
                                     "temp_fallback": 0.01}
                except RuntimeError as e2:
                    last = e2
            wait = min(90, 3 * 2 ** attempt + random.random() * 5)
            time.sleep(wait)
    raise last


# --------------------------------------------------------------------------- #
# Parsing + validation
# --------------------------------------------------------------------------- #
THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def parse_reading(content):
    """Validate against the schema. Returns dict or raises ValueError."""
    c = THINK_RE.sub("", content or "")
    m = re.search(r"\{.*\}", c, re.DOTALL)
    if not m:
        raise ValueError("no JSON object found in output")
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON: {e}")
    if not isinstance(d, dict) or "room_reading" not in d or \
            "private_displacement" not in d:
        raise ValueError("missing room_reading/private_displacement keys")
    out = {}
    for part, lo, hi in (("room_reading", 0, 100),
                         ("private_displacement", -100, 100)):
        src = d[part]
        if not isinstance(src, dict):
            raise ValueError(f"{part} is not an object")
        vals = {}
        for dial in DIALS:
            if dial not in src:
                raise ValueError(f"{part}.{dial} missing")
            v = src[dial]
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ValueError(f"{part}.{dial} not numeric: {v!r}")
            if not (lo - 5 <= v <= hi + 5):
                raise ValueError(f"{part}.{dial} out of range: {v}")
            vals[dial] = float(min(hi, max(lo, v)))
        out[part] = vals
    return out


def elicit_one(reader, window_id, level, pass_tag):
    rid, endpoint, model = reader
    window = WINDOWS[window_id]
    d = os.path.join(RDIR if level == "P0" else SDIR, rid)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{window_id}.{level if level != 'P0' else 'pass' + pass_tag}.json")
    if os.path.exists(path):
        with open(path) as f:
            cached = json.load(f)
        return cached.get("ok", False)

    sys_, user = build_prompt(window, level)
    messages = [{"role": "system", "content": sys_},
                {"role": "user", "content": user}]
    record = {"reader": rid, "model": model, "window": window_id,
              "level": level, "pass": pass_tag}
    parsed, meta, raw = None, None, None
    for repair in range(3):  # 1 fresh + 2 repair attempts
        try:
            raw, meta = call_with_retries(endpoint, model, messages)
            parsed = parse_reading(raw)
            break
        except ValueError as e:
            record["parse_error"] = str(e)
            messages = messages[:2] + [
                {"role": "assistant", "content": (raw or "")[:600]},
                {"role": "user", "content":
                 f"That output was invalid ({e}). Output ONLY the strict "
                 f"JSON object with both required keys and all seven dials "
                 f"({', '.join(DIALS)}), integer values. No prose. No fences."}]
        except RuntimeError as e:
            record["net_error"] = str(e)[:300]
            break
    record["ok"] = parsed is not None
    record["parsed"] = parsed
    record["meta"] = meta
    record["raw"] = (raw or "")[:2000]
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(record, f, ensure_ascii=False)
    os.replace(tmp, path)
    return record["ok"]


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    jobs = []
    for reader in READERS:
        rid = reader[0]
        if only and rid not in only:
            continue
        for wid in WINDOWS:                      # canonical: 2 passes
            jobs.append((reader, wid, "P0", "1"))
            jobs.append((reader, wid, "P0", "2"))
        for wid in SWEEP_WINDOWS:                # paraphrase sweep
            for lvl in ("P1", "P2", "P3"):
                jobs.append((reader, wid, lvl, "s"))
    random.Random(20260819).shuffle(jobs)  # interleaved load, registered seed
    print(f"{len(jobs)} elicitation jobs ({len(READERS)} readers)")
    done = [0]
    t0 = time.time()

    def run(job):
        try:
            ok = elicit_one(*job)
        except Exception as e:  # never kill the pool
            print(f"  job error {job[0][0]}/{job[1]}/{job[2]}{job[3]}: {e}",
                  flush=True)
            ok = False
        done[0] += 1
        if done[0] % 25 == 0:
            print(f"  {done[0]}/{len(jobs)} ({time.time()-t0:.0f}s)", flush=True)
        return ok

    with cf.ThreadPoolExecutor(CONCURRENCY) as ex:
        results = list(ex.map(run, jobs))
    fails = len(jobs) - sum(results)
    print(f"complete: {sum(results)} ok, {fails} failed "
          f"({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
