---
name: optimize-p95
description: Profiler-driven performance optimization loop using a dynamic workflow. Use ONLY when the user explicitly invokes /optimize-p95 or says "optimize p95" / "run the perf loop". Do not trigger for general performance questions.
---

# Optimize p95 (dynamic workflow)

Goal: hit the user's stated latency target (default: p95 < 300ms) with measured proof.

1. Confirm the target metric and the benchmark command that reports p95. If no
   benchmark exists, create a minimal reproducible one first — the loop cannot
   self-verify without it.
2. Detect the stack from repo markers before picking tools — do not assume:
   - `pyproject.toml`/`requirements.txt` → Python: profile with py-spy
     (fallback cProfile), benchmark with pytest-benchmark or hyperfine.
   - `package.json` → Node/TS: profile with clinic flame or 0x
     (fallback `node --cpu-prof`), benchmark with autocannon (HTTP) or
     hyperfine.
   - `go.mod` → Go: pprof (`go test -cpuprofile` or net/http/pprof),
     benchmark with `go test -bench` or vegeta (HTTP).
   - `Cargo.toml` → Rust: cargo flamegraph, benchmark with criterion or
     hyperfine.
   - Mixed repo: profile the service the p95 target refers to; ask if
     ambiguous.
   Install the chosen profiler if missing; verify it runs before starting
   the loop.
3. Launch a dynamic workflow (use "ultracode" if needed) with this loop:
   profile → identify top hotspot → apply one fix → re-run benchmark →
   compare p95 → repeat until target met. Don't stop until the benchmark
   confirms the target.

   Role hierarchy (optional — assumes a multi-agent setup with subagents and an
   external Codex CLI; on a single-agent setup run the loop yourself):
   - **Fable (this session) = chief architect.** Owns the loop, reads profiler
     output, decides which hotspot to attack and when the target is met. Does
     not write the fixes itself.
   - **Codex = solution architect.** For each hotspot, Fable consults Codex
     (`codex exec`) for the fix design; Fable reconciles it with its own plan
     and issues one agreed instruction.
   - **Opus subagents = developers.** Spawn with `model: opus`; they implement
     exactly the agreed instruction in their own worktree — no improvising
     beyond it.
4. Each candidate fix runs in its own Opus subagent/worktree; the chief
   architect keeps only changes that measurably improve p95.
5. Report: before/after p95, list of changes kept, profiler evidence. Write
   the full log to a file; reply with the path + final numbers only.

Constraints: cap token usage if the user gives a budget; simplest fix first
per design-best-practices; no speculative micro-optimizations.

## Unforgiving mode (always on — no easy passes)

- **Never** relax the target, change the benchmark, or shrink its scope
  mid-run to make the number pass. Target set at start = target at end.
- p95 must come from the **same benchmark, same conditions** every run —
  no cherry-picked warm runs, no reduced load, no measuring a subset.
- Every kept change must show a measured improvement in its own run;
  revert changes that don't. No "probably faster" reasoning.
- Done means the benchmark output showing p95 under target, pasted in the
  final report. If unreachable, report the honest gap and remaining
  hotspots — never declare success without the passing numbers.
