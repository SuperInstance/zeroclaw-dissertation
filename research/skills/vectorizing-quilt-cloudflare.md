# Vectorizing: "quilt-cloudflare" — status note

⚠️ **`/home/eileen/projects/quilt-cloudflare/` does not exist on this host.**
Verified 2026-08-19 (`find` found only `~/projects/quilt` and `~/projects/quilt-rust`).
The Cloudflare-backed Quilt variant referenced in my orientation brief is either
not yet built, lives elsewhere, or was renamed. This file records what actually exists.

## What exists: `/home/eileen/projects/quilt/` (TS, v0.2.0)
A reactive, typed, cellular runtime — "a spreadsheet where every cell is a live,
addressable capability. The grid is the runtime." Packages: `packages/core`
(engine), `packages/cli`, `packages/mcp` (whole sheet is an MCP server; every
named cell is an MCP tool), `packages/tui`. Rust port at `~/projects/quilt-rust`
(axum server, TUI, rhai-sandboxed cells, ~high-throughput compiled evaluation).

- Sheets are YAML; cells are value/formula/api/program/sensor/listener/router/io.
- Cell references are stable **addresses**, not coordinates.
- Reactive by default; per-caller memoization; routing on caller context
  (`caller.row > 10` → Model A).
- `grep` for Vectorize/D1/R2/KV/Cloudflare across `docs/`, `packages/*/src`,
  `examples/`: **no hits** — current Quilt has no Cloudflare storage bindings.

## How a "Quilt on Cloudflare" would map (design inference)
If/when built, the natural mapping given the fleet's existing patterns:
- Sheet cells → Worker routes / Durable Objects per cell or per sheet
- `value`/`sensor` cells → KV or D1 (small state) / R2 (blobs)
- Vector cells (a cell whose value is an embedding) → Vectorize index, following
  crab-traps' ID-prefix convention (`cell-<addr>` vectors, metadata = cell address)
- Reactive recompute → DO alarms or cron triggers, like crab-traps' hourly pass
- The manifesto's "sensor" cell type is the natural home for a JEPA dial: a cell
  whose value is the live reading of a conversation's latent state

## JEPA relevance
Quilt's paradigm — addressable live cells, reactive rewiring, the sheet as runtime —
is the orchestration layer for a "co-linear-algebra dataset": each conversation's
JEPA readings could be cells; the sameness-weight between two conversations a
reactive `edges`-style computation that re-fires when either reading changes.
