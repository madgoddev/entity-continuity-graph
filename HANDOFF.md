# EntityContinuityGraph handoff

This is a standalone, contract-only GenLayer project with no frontend or GitHub dependency.

## v4 release

- Source SHA-256: `0CED2851AEB13E3041D8989ADB30AB16F69D51BA34988CF5D0427EFF1ACDA952`
- Size: 30,964 bytes; 772 lines
- ABI: 14 public methods (13 views, one write, no constructor parameters)
- Schema: `ENTITY_CONTINUITY_GRAPH/4.0`
- Policy: `ECG-RELATIONSHIP-POLICY/4`
- Identity domain: `ECG-CONTENT-ADDRESS/4`
- Local verification: 54 direct plus three five-validator GLSim tests

Every validator now makes one LLM call and must exactly reproduce the leader's minimal relationship/direction claim. `claim_code` is deterministic. No model-authored confidence, citations, rationale, or issues are accepted or stored.

Independent frozen-source audit returned `GO`. The checked-in StudioNet and Bradbury records verify the same exact v4 source, ABI, protocol, and semantic write/readback. Both superseded v3 Bradbury smokes listed in `docs/VERIFICATION.md` ended `UNDETERMINED / DISAGREE` with zero state; the redesigned v4 Bradbury deployment and smoke both finalized with agreed, execution-successful outcomes.

## Completed release gates

1. Independent audit of the exact source hash returned `GO`.
2. Lint, schema deep comparison, strict typecheck, direct tests, and five-validator GLSim passed without changing source bytes.
3. Exact-byte deployments finalized successfully on StudioNet and Bradbury.
4. Retrieved source, ABI, `version`, `policy`, `limits`, and pre-smoke zero state matched exactly on both networks.
5. One reviewed public-only fixture write finalized successfully on each network, followed by exact observation, checkpoint, history, fingerprint-gate, and count readback.
6. The checked-in evidence is curated and excludes raw validator receipts, secrets, node configuration, and environment data.
7. Distribution packaging must continue to use the explicit allowlist.

Downstream consumers must pin network, contract address, policy, finalized state, observation ID, and result fingerprint. The latest-pair pointer remains advisory.
