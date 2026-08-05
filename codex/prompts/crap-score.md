# crap-score — CRAP-metric reduction loop

Goal: every function's CRAP below threshold (default **8**; stretch target 6).
CRAP(m) = CC² × (1 − coverage)³ + CC — high complexity is forgivable only if
well covered; uncovered complexity is not.

1. Detect stack from repo markers and produce per-function scores:
   - **Python** (`pyproject.toml`/`requirements.txt`): needs `radon` + `coverage`.
     ```
     radon cc -j <src> > /tmp/radon.json
     coverage run -m pytest -q && coverage json -o /tmp/coverage.json
     python ~/.claude/skills/crap-score/scripts/crap_py.py /tmp/radon.json /tmp/coverage.json --threshold 8
     ```
     Exit 1 = functions still over threshold (loop gate).
   - **Go** (`go.mod`): `gocyclo -over 0 .` for CC + `go test -coverprofile=c.out ./...`
     then `go tool cover -func=c.out`; join per function and compute CRAP yourself.
   - **TS/Node** (`package.json`): needs `eslint` + `c8` (via `npx --yes`).
     ```
     npx --yes eslint <src> -f json --rule '{"complexity":["warn",0]}' > /tmp/eslint.json
     npx --yes c8 --reporter=json <test cmd>   # writes coverage/coverage-final.json
     python ~/.claude/skills/crap-score/scripts/crap_ts.py /tmp/eslint.json coverage/coverage-final.json --threshold 8
     ```
     Exit 1 = functions still over threshold (loop gate).
2. Report the baseline: worst 10 functions with file:line, CC, coverage, CRAP.
3. Loop — one function at a time, worst first (Bob's order):
   a. **Cover first**: if coverage is low, write characterization tests until
      the function's lines are covered. Never refactor uncovered code.
   b. **Split second**: only if CC alone keeps CRAP over threshold, extract
      smaller well-named functions (few args), keeping tests green.
   c. Re-run the scorer; confirm the number dropped and nothing else regressed.
4. Stop when the scorer exits 0. Write before/after table + changes to a file;
   reply with the path and the headline numbers.

Constraints: no behavior changes during refactors (tests must stay green);
simplest split that clears the threshold, nothing speculative.

## Unforgiving mode (always on — no easy passes)

- **Never** raise the threshold, exclude files, or shrink scope mid-run to
  make the number pass. The threshold set at start is the threshold at end.
- Coverage must come from **real assertions on behavior** — a test that
  executes lines without asserting outcomes does not count; delete it and
  write a real one. No `assert True`, no snapshot-everything, no mocking the
  function under test.
- Splits must **move complexity into tested code**, not hide it: every
  extracted function gets its own score and must also clear the threshold.
  No dumping branches into an untested helper.
- Re-run the **full** scorer after every change; if any other function
  regressed, fix that before proceeding. No "net improvement" excuses.
- Done means exit 0 on a clean full run, pasted in the final report. If it
  can't be reached, report the honest remaining offenders — never declare
  success without the passing output.
