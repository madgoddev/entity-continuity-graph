# Testing

## Results

```text
GenVM lint / SDK validation: PASS
ABI extraction:              PASS (14 methods: 13 view, 1 write)
Strict typecheck:             PASS (0 diagnostics)
Direct mode:                  PASS (54/54)
Five-validator GLSim:         PASS (3/3)
Total automated tests:        PASS (57/57)
```

Direct tests cover v4 content identities, every relationship and both successor directions, explicit `UNRESOLVED`, exact independent match and mismatch, hostile or extra model output, malformed leader calldata, and an instrumented assertion that the validator invokes exactly one LLM prompt. They also cover append-only history, non-forking same-submitter corrections, pagination, fingerprint matching, duplicate-key rejection at multiple depths, strict schemas, bounded JSON, public-only policy, closed provenance/capture labels, and temporal validation.

The GLSim suite uses exactly five validators and asserts unanimous agree votes for:

- a `SAME_ENTITY` checkpoint;
- a directed `SUCCESSOR:A_TO_B` correction and pair history; and
- an `UNRESOLVED:NONE` checkpoint.

Mocked model output keeps integration tests reproducible; GLSim still executes the contract's leader and custom validator path for all five validators.

## Reproduction

```powershell
genvm-lint check contracts/entity_continuity_graph.py
genvm-lint schema contracts/entity_continuity_graph.py --output abi/entity_continuity_graph.abi.json
genvm-lint typecheck contracts/entity_continuity_graph.py --strict
pytest tests/direct -q
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_glsim_5.ps1
```

The Windows harness starts an isolated hidden five-validator GLSim process, refuses an occupied port, applies the project-local `genlayer-test==0.29.2` compatibility shim, runs only integration tests, and stops the simulator in a `finally` block.
