# Verification Record

Verification date: 2026-08-12

- Contract: `contracts/entity_continuity_graph.py`
- SHA-256: `0CED2851AEB13E3041D8989ADB30AB16F69D51BA34988CF5D0427EFF1ACDA952`
- Size: 30,964 bytes
- Lines: 772
- Schema: `ENTITY_CONTINUITY_GRAPH/4.0`
- Policy: `ECG-RELATIONSHIP-POLICY/4`
- Identity domain: `ECG-CONTENT-ADDRESS/4`
- Runner: pinned `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Static and local execution

- GenVM lint and SDK validation passed.
- Strict typecheck passed with zero diagnostics.
- Generated ABI is deep-equal to the checked-in ABI: 14 public methods, 13 views, one write, no constructor parameters.
- ABI SHA-256: `DE015B872811DCFF3E7F2BD0598EEB44FF547E7FA0E582B7E15DAE2C17D38009`.
- Direct tests: 54 passed.
- Five-validator GLSim: 3 passed.

The linter's only notice was informational: a newer runner exists. This candidate retains the concrete runner hash against which it was tested.

## Network status

Both checked-in deployment records verify exact v4 source and ABI, finalized successful deployment and semantic write, content-addressed record/history, and checkpoint gates:

| Network | Contract | Deployment transaction | Smoke transaction | Outcome |
|---|---|---|---|---|
| StudioNet | `0xb4730Eb80E8996942d0b168204c48EE265F775F5` | `0xe8979217f8860cd53dad2888f8d6e5078236af3d054a10bb9f649b9178a43070` | `0x38230e662113cfbf81ae5ec739585d5ba4b9f82ea53d8824a2f9fe7cb3161326` | Finalized majority agree; exact readback passed |
| Bradbury | `0xe1e670607C75F8d5aB531DFB3000fD863Db851F4` | `0x0d5994b7a34c4fb6701b22daa31e2eeb3cb445792138fdffe9a60c6bb3094e38` | `0x4c75735f10618c7772b067a748076a26b34a4f45eec80c9602ffc9e8f53d987b` | Finalized agree and successful execution; exact readback passed |

Bradbury deployment received five agree votes. The smoke received four agree votes and one timeout; the transaction still finalized `AGREE / FINISHED_WITH_RETURN`. Latest-final readback verified `SUCCESSOR:A_TO_B`, all six v4 content addresses, one stored observation, one pair-history row, index zero, no superseding observation, an exact-fingerprint `true` gate, and altered/unknown `false` gates.

The two v3 Bradbury smoke attempts below both ended `UNDETERMINED / DISAGREE` with successful leader returns and zero stored observations:

| Transaction | Rounds | Last revealed votes |
|---|---:|---|
| `0xd8056970c1e7ee2ae398a8f7a5251ddfb1b2fbf6015337fa7c5b8883e8e5380c` | 2 | `AGREE`, `TIMEOUT`, 3× `DETERMINISTIC_VIOLATION` |
| `0x20e9a3cbca60ceef6a31760b2aac92c1bae7d52dfe6d9c24dd1ce07a1de6906d` | 4 | 2× `TIMEOUT`, 3× `DETERMINISTIC_VIOLATION` |

They are diagnostic evidence for the superseded two-validator-call v3 design, not release evidence. The v4 independent audit and exact-byte StudioNet and Bradbury deployment/write/readback gates now pass.
