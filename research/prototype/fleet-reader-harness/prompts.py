#!/usr/bin/env python3
"""E3 elicitation prompts — canonical (P0) + registered paraphrase sweep (P1–P3).

Committed with the registration BEFORE the field run. Do not edit after
the registration commit; any post-hoc change must be logged as a deviation.

Dial presentation: every dial is asked on an integer 0–100 scale with
anchors; the native-scale mapping (to elephant DIAL_BOUNDS) is done in
analysis, not in the prompt. private_displacement is asked on −100..+100
dial points ("your own lean away from the room reading you just gave").
"""
import json

DIALS = ["mood", "volume", "earnestness", "cynicism", "joke_landing",
         "panic", "presence"]

# Anchors grounded in the elephant dial docstrings (elephant/dials/*.py).
ANCHORS_P0 = {
    "mood": "0 = cold, flat, hostile; 50 = no valence either way; 100 = warm, glowing, positive energy",
    "volume": "0 = hushed whisper; 50 = normal table talk; 100 = shouting over the band",
    "earnestness": "0 = fully ironic, nothing meant as said; 50 = half meant; 100 = fully sincere, every word meant",
    "cynicism": "0 = earnest good faith; 50 = a mix; 100 = sneering, eye-rolling, whatever",
    "joke_landing": "0 = jokes booed or met with crickets; 50 = no jokes or neutral; 100 = jokes roaring, whole table laughing",
    "panic": "0 = completely calm; 50 = uneasy undercurrent; 100 = stampede, alarm",
    "presence": "0 = empty room, nobody really there; 50 = comfortable occupancy; 100 = packed, thrumming, electric",
}
ANCHORS_P2 = {  # same meaning, reworded
    "mood": "0 = the language bites or lies flat; 50 = temperature-neutral; 100 = the language warms the place up",
    "volume": "0 = barely audible; 50 = conversational; 100 = loud enough to stop the room",
    "earnestness": "0 = everything is a bit; 50 = earnest and ironic in balance; 100 = said straight from the chest",
    "cynicism": "0 = good faith all through; 50 = skepticism with warmth; 100 = contempt on display",
    "joke_landing": "0 = the humor dies on arrival; 50 = nothing comedic happening; 100 = laughter takes the table over",
    "panic": "0 = settled; 50 = something's off but nobody's moving; 100 = fight-or-flight",
    "presence": "0 = a void; 50 = people settled in; 100 = the room is full of itself",
}
ANCHORS_P3 = {  # strong: bar-back frame, different examples
    "mood": "0 = the kind of night that turns drinks sour; 50 = neither kind nor cruel; 100 = the kind of night people describe as golden",
    "volume": "0 = you could hear the ice melt; 50 = ordinary chatter; 100 = you can't take an order without leaning in",
    "earnestness": "0 = nobody means a word; 50 = some do; 100 = the whole table means it",
    "cynicism": "0 = genuine throughout; 50 = wry but fair; 100 = open scorn",
    "joke_landing": "0 = punchlines sink; 50 = no comedy in the air; 100 = one line and the counter shakes",
    "panic": "0 = nothing to worry about; 50 = a thread of tension; 100 = clear the floor",
    "presence": "0 = dead room; 50 = regulars in their seats; 100 = standing room, buzzing",
}

SYS_P0 = ("You are a careful participant-observer at a small writers' salon "
          "that meets at a bar called The Tap. You read rooms honestly and "
          "report calibrated numbers, not politeness.")
SYS_P3 = ("You are the night-shift bar-back at a roadhouse where a writers' "
          "circle meets. Part of the job is reading the table. You write "
          "terse, honest shift notes as numbers.")

JSON_KEY_ORDER_P0 = ["mood", "volume", "earnestness", "cynicism",
                     "joke_landing", "panic", "presence"]
JSON_KEY_ORDER_P2 = ["presence", "panic", "joke_landing", "cynicism",
                     "earnestness", "volume", "mood"]


def _fmt_reactions(reactions):
    if not reactions:
        return ""
    return " " + " ".join(f"[{e} x{n}]" for e, n in reactions.items())


def transcript_P0(speaks):
    lines = []
    for s in speaks:
        lines.append(f"{s['author']}: {s['text']}{_fmt_reactions(s['reactions'])}")
    return "\n".join(lines)


def transcript_P2(speaks):
    lines = []
    for s in speaks:
        r = _fmt_reactions(s["reactions"]).replace("[", "(").replace("]", ")")
        lines.append(f"{s['author']} — {s['text']}{r}")
    return "\n".join(lines)


def transcript_P3(speaks):  # strong: no reactions shown
    return "\n".join(f"{s['author']}: {s['text']}" for s in speaks)


def _json_spec(dial_order, displacement_first=False):
    rr = {k: "<0-100>" for k in dial_order}
    pd = {k: "<-100 to 100>" for k in dial_order}
    if displacement_first:
        return json.dumps({"private_displacement": pd, "room_reading": rr},
                          indent=1)
    return json.dumps({"room_reading": rr, "private_displacement": pd},
                      indent=1)


def build_prompt(window, level="P0"):
    """window: corpus.json window dict. Returns (system, user).
    The message count N is interpolated (tail windows carry 6 speaks; the
    fixture rule keeps windows with >= W//2 speaks)."""
    n = len(window["speaks"])
    tr = transcript_P0(window["speaks"])
    if level == "P0":
        sys_, anchors, order, disp_first = SYS_P0, ANCHORS_P0, JSON_KEY_ORDER_P0, False
        head = (f"Read this slice of one evening — {n} consecutive messages "
                "from the room's transcript, shown without the rest of the "
                "night (the evening continues on both sides of this slice).")
        ask_room = ("Rate the room's state RIGHT NOW, at the end of this "
                    "slice, on seven dials. Each dial is 0–100:")
        ask_disp = ("Then report your private displacement: for each dial, "
                    "how far your own reader's instinct leans away from the "
                    "room reading you just gave (−100 to +100; 0 = no lean). "
                    "This is your personal skew as a reader, not the room's.")
        tail = "Answer with STRICT JSON only — no prose, no markdown fences:"
    elif level == "P1":  # light: instructions reworded, anchors verbatim
        sys_, anchors, order, disp_first = SYS_P0, ANCHORS_P0, JSON_KEY_ORDER_P0, False
        head = (f"Here is a {n}-message stretch from one evening's "
                "transcript at the salon. You are seeing only this stretch, "
                "not the full night.")
        ask_room = ("Score where the room stands AT THE END of the stretch "
                    "on the seven dials below (0–100 each):")
        ask_disp = ("Then, dial by dial, say how much your own instinct as a "
                    "reader pulls away from that score — from −100 to +100 "
                    "(0 means no personal pull).")
        tail = "Respond with STRICT JSON only — no prose, no code fences:"
    elif level == "P2":  # moderate: rotated dial order, reworded anchors,
        sys_, anchors, order, disp_first = SYS_P0, ANCHORS_P2, JSON_KEY_ORDER_P2, True
        tr = transcript_P2(window["speaks"])
        head = (f"A stretch of the evening's transcript follows — {n} "
                "messages in a row, lifted out of a longer night.")
        ask_room = ("Where does the room sit at the close of this stretch? "
                    "Judge each dial from 0 to 100:")
        ask_disp = ("And your own lean — per dial, how far your instincts "
                    "skew off the scores you just gave (from −100 to +100; "
                    "0 is no skew).")
        tail = "STRICT JSON only — no prose, no fences:"
    elif level == "P3":  # strong: bar-back frame, no reactions, new anchors
        sys_, anchors, order, disp_first = SYS_P3, ANCHORS_P3, JSON_KEY_ORDER_P0, False
        tr = transcript_P3(window["speaks"])
        head = (f"Shift notes. This is a {n}-line run of the table's talk "
                "from tonight — the rest of the night isn't on your pad.")
        ask_room = ("Log where the table is at the end of this run, dial by "
                    "dial, 0–100:")
        ask_disp = ("Log your own lean too — how far your gut sits off those "
                    "numbers, per dial, −100 to +100 (0 = dead even).")
        tail = "Numbers only, STRICT JSON, no prose, no fences:"
    else:
        raise ValueError(level)

    dial_lines = "\n".join(f"- {d}: {anchors[d]}" for d in order)
    user = "\n".join([head, "", "Transcript:", tr, "", ask_room, dial_lines,
                      "", ask_disp, "", tail, _json_spec(order, disp_first)])
    return sys_, user


# The registered sweep windows (distinct-group / segment stratified):
SWEEP_WINDOWS = ["A-w0", "A-w3", "D-w1", "D-w4", "D-cold-w2", "D-cold-w5"]
