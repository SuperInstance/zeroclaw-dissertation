# Quilt — The Grid Is the Runtime

*Source: `/home/eileen/projects/quilt/README.md` (github.com/SuperInstance/quilt, TS + Rust ports; also `/home/eileen/projects/quilt-cloudflare/`)*

## The one line

**A spreadsheet where every cell is a live, addressable capability. The grid is the runtime.** A cell is not a value; a cell is a **contract** — a stable address you can plug anything into. A sheet is a YAML file, and that file *is* the whole system: data, logic, I/O, routing, alerting.

## The mental model (5 layers of "addressing as composition")

```
Layer 0  ADDRESS           stable id, not a coordinate. A name.
Layer 1  SPATIAL           row / column carry context. Position is policy.
Layer 2  REACTIVE          when an address changes, dependents re-evaluate.
Layer 3  BIDIRECTIONAL     same address is readable AND writable.
Layer 4  COMPOSING         writing an address IS binding to it.
```

## The 8 cell kinds

| Kind | What it is | Evaluator |
|---|---|---|
| `value` | static data, no deps | direct |
| `formula` | pure reactive expression, lazily recomputed on change | `new Function` |
| `api` | HTTP/model/MCP endpoint fetched on call | async fetch |
| `program` | inline async JavaScript (`input`, `caller`, `runtime.get/set/call`) | AsyncFunction |
| `sensor` | push-only inbound stream; adapter writes, formulas read | external adapter |
| `io` | bidirectional port (webhook, GPIO, actuator) | external adapter |
| `listener` | eager trigger on watched-cell change | engine propagation |
| `router` | caller-aware policy: rules like `caller.row > 10 → route: fast` | `eval_when` |

## How formulas compute

- Dependency edges are **auto-detected by scanning the expression** — never declared. `=temp * 9/5 + 32` binds the formula to `temp`.
- Pure cells are **lazy** (Excel-style: change marks dependents stale; next read recomputes). Listeners are **eager** (fire the instant a watched cell changes). Effectful cells (`api`/`program`/`router`) run when called and cache **per caller context** (`row`, `column`, `identity.id`, `identity.tags`) — same cell, different cached answers per caller.
- Graph is a flat `Map<CellId, Cell>` with explicit `dependencies`/`dependents` sets — cycles allowed for effectful feedback (sensor→formula→listener→actuator→sensor); pure chains must stay acyclic.
- `CellValue` is `{data, status, error, effects, computed_at}` — the value knows its freshness and its audit trail (effects = what the cell did: network, storage, model, compute).
- Engine API: `loadSheet`, `get`, `set`, `call`, `push`, `subscribe`, `register` (dynamic cell registration at runtime — agents defining cells).

## Agents

The whole sheet is an **MCP server**; every named cell is an MCP tool (`cell__<id>`), the sheet a resource at `quilt://<sheet>/sheet`. Caller context (row/identity) travels with every call, so one sheet serves many tenants/tiers without forking. Humans and agents share one grid: agent writes a cell, human sees the write; human overrides, agent sees it on next read.

The **jazz→classical flywheel**: start with an LLM cell, watch the calls, distill the common cases into a formula, watch cost drop — a visible, editable decomposition process.

## Worked pattern (boat-autopilot)

```yaml
heading        [sensor]   nmea:/dev/ttyUSB0
target_heading [value]    270
error          [formula]  =((target_heading - heading + 540) % 360) - 180
rudder         [formula]  =clamp(error * 0.5, -30, 30)
rudder_cmd     [io]       port: rudder_actuator, direction: out
```

Change `target_heading` → dependents rewire → actuator commanded. Editing the file IS commanding the system.

## Caveats that matter for grafting work onto it

- TS engine is **not sandboxed** (`new Function`/`AsyncFunction` run in-host); Rust port uses rhai (sandboxed); WASM sandbox planned.
- CLI is stateless — persistence is the YAML file; liveness is a harness / `serve --mcp` session / TUI / simulator.
- Per-context memoization means effectful cells don't auto-recompute when upstream changes — you must vary context or `set`.
- ~50k ops/s TS, compiled Rust for higher throughput.
