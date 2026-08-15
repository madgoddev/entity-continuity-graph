# Security and Design Audit

Audit date: 2026-08-12

Candidate source SHA-256: `0CED2851AEB13E3041D8989ADB30AB16F69D51BA34988CF5D0427EFF1ACDA952`

## Current disposition

Local verification is clean, independent review of the exact v4 freeze returned `GO`, and exact deployment plus semantic write/readback pass on StudioNet and Bradbury.

## v4 liveness redesign

Two v3 Bradbury smoke transactions ended `UNDETERMINED / DISAGREE` despite successful leader returns and made no state change:

- `0xd8056970c1e7ee2ae398a8f7a5251ddfb1b2fbf6015337fa7c5b8883e8e5380c`: two rounds; last revealed votes were one agree, one timeout, and three deterministic violations.
- `0x20e9a3cbca60ceef6a31760b2aac92c1bae7d52dfe6d9c24dd1ce07a1de6906d`: four rounds; last revealed votes were two timeouts and three deterministic violations.

The v3 validator made two LLM calls and accepted ancillary leader fields only after a separate grounding response. That expanded execution and deterministic-comparison surface. v4 replaces it with one independent LLM call and a three-field canonical consensus claim whose `claim_code` is contract-derived.

## Reviewed properties

1. **Exact minimal consensus claim.** Model output contains only relationship and direction. Unknown, missing, extra, or internally inconsistent fields reject.
2. **Independent exact match.** Each validator classifies the full evidence bundle without receiving leader prose and agrees only on exact claim equality.
3. **One validator LLM call.** Direct instrumentation asserts one classifier prompt during validator execution.
4. **No model-authored ancillary facts.** Confidence, citations, rationales, and issue codes are not accepted or stored.
5. **Conservative unresolved path.** `UNRESOLVED:NONE` is a first-class exact claim and never equals a decisive claim.
6. **Prompt-injection boundary.** Canonical JSON is delimited as untrusted; prompts prohibit following embedded instructions, browsing, and hidden knowledge.
7. **Strict public input.** JSON size/depth, duplicate keys, dates, document count, closed enums, and public-only/privacy attestations are enforced before consensus.
8. **v4 content identity.** All address preimages bind the v4 policy and explicit address-domain version and use the `urn:ecg4:*` namespace.
9. **Append-only corrections.** Exact duplicates revert; corrections are same-pair, same-submitter, time-ordered, reasoned, and non-forking.
10. **Pinned downstream gate.** `matches_checkpoint` checks the exact result fingerprint; latest-pair state remains explicitly advisory.
11. **No network fetch or privileges.** The contract has no URL fetch, owner, admin, upgrade, delete, payment, or private evidence method.

## Local verification

- Source: 30,964 bytes, 772 lines.
- GenVM lint and SDK validation: pass.
- ABI: 14 public methods, 13 views, one write, zero constructor parameters.
- ABI SHA-256: `DE015B872811DCFF3E7F2BD0598EEB44FF547E7FA0E582B7E15DAE2C17D38009`.
- Strict typecheck: zero diagnostics.
- Direct tests: 54 passed.
- Five-validator GLSim: 3 passed.
- Combined: 57 passed.

GLSim uses reproducible mock model outputs but runs the real custom consensus path across five validators. It covers `SAME_ENTITY`, directed `SUCCESSOR` correction history, and `UNRESOLVED`.

## Network verification

- StudioNet deployment `0xe8979217f8860cd53dad2888f8d6e5078236af3d054a10bb9f649b9178a43070` and smoke `0x38230e662113cfbf81ae5ec739585d5ba4b9f82ea53d8824a2f9fe7cb3161326` finalized with majority agreement and successful execution.
- Bradbury deployment `0x0d5994b7a34c4fb6701b22daa31e2eeb3cb445792138fdffe9a60c6bb3094e38` created contract `0xe1e670607C75F8d5aB531DFB3000fD863Db851F4`, finalized `AGREE / FINISHED_WITH_RETURN`, and received five agree votes.
- Bradbury smoke `0x4c75735f10618c7772b067a748076a26b34a4f45eec80c9602ffc9e8f53d987b` finalized `AGREE / FINISHED_WITH_RETURN` with four agree votes and one timeout.
- Latest-final readback on both networks matched the exact v4 source, ABI, protocol, independently derived content addresses, `SUCCESSOR:A_TO_B` checkpoint, pair history, count/index, and exact/altered/unknown fingerprint gates.

Curated records are in `deployments/studionet.json` and `deployments/bradbury.json`. Raw receipts, validator configuration, and signing material are deliberately excluded.

## Residual risks

- Caller excerpts can be forged, truncated, mistranscribed, stale, or selectively chosen.
- Semantic consensus can still be wrong or correlated across validators.
- `UNRESOLVED` is prompt-enforced for ambiguity; deterministic code cannot itself prove evidence sufficiency.
- Content addresses identify submitted canonical bytes, not real-world organizations or source authenticity.
- The privacy attestation is not a content scanner.
- Consumers must respect graph scope, context, date, submitter, supersession, network, policy, observation ID, and result fingerprint.

This contract is suitable only as an advisory evidence graph or a pinned input to a downstream system with its own risk policy. It is not sole proof for legal identity, ownership, sanctions, asset transfer, authority, or irreversible high-value action.
