# EntityContinuityGraph

EntityContinuityGraph is a standalone GenLayer Intelligent Contract that records cautious, evidence-bounded observations about whether two organization descriptors appear to be the same entity, successors, affiliates, unrelated, or unresolved.

It is an advisory graph primitive, not a company registry or legal identity oracle. It has no frontend, administrator, payout, or arbitrary URL fetcher.

## Why GenLayer

Organization continuity is often expressed indirectly across public notices, filings, court records, archived pages, and independent reports. The relevant distinction is semantic: a renamed organization can remain the same entity, a new organization can be a successor, and an affiliate remains distinct.

Protocol v4 uses a deliberately minimal consensus claim:

```json
{
  "relationship": "SAME_ENTITY | SUCCESSOR | AFFILIATE | UNRELATED | UNRESOLVED",
  "succession_direction": "A_TO_B | B_TO_A | NONE"
}
```

The leader and every independent validator classify the complete canonical evidence bundle. Each validator makes exactly one LLM call and must independently return the exact same relationship and direction. The contract derives `claim_code` deterministically. It rejects extra fields, unknown values, invalid direction combinations, and any mismatch.

Model-authored confidence, citations, rationales, and issue codes are neither accepted nor stored. The submitted public evidence remains in the immutable record so downstream users can inspect the exact material behind a claim.

The current schema is `ENTITY_CONTINUITY_GRAPH/4.0`, policy is `ECG-RELATIONSHIP-POLICY/4`, and address domain is `ECG-CONTENT-ADDRESS/4`.

## Relationship semantics

| Value | Narrow meaning |
|---|---|
| `SAME_ENTITY` | The excerpts materially support continuity of one organization across labels or time. |
| `SUCCESSOR` | The excerpts materially support succession. `A_TO_B` means B succeeds A; `B_TO_A` means A succeeds B. |
| `AFFILIATE` | The excerpts support affiliation while preserving distinct identities. |
| `UNRELATED` | The excerpts affirmatively support separateness in the declared context. Missing evidence alone is insufficient. |
| `UNRESOLVED` | The excerpts do not adequately support exactly one stronger classification. |

These observations do not establish ownership, control, beneficial ownership, liability, registry status, authenticity, or authority to act.

## Immutable input and graph

`observe(...)` accepts a graph-scope slug, two strict JSON entity descriptors, an observation date, a bounded question context, a versioned public-only evidence bundle, and optional correction linkage. The external input schema is unchanged from v3.

All JSON is size- and depth-bounded, rejects duplicate keys and non-standard numeric constants, and uses closed provenance/capture enums. Evidence cannot postdate the observation. The contract never follows source locators and treats provenance labels as caller assertions.

Every entity, document, evidence bundle, ordered pair, observation, and result receives a v4 domain-separated SHA-256 address under `urn:ecg4:*`. These addresses identify canonical submitted content, not real-world authenticity.

Observations are append-only. A correction must name an existing same-pair observation from the same submitter, include a reason, preserve time order, and cannot fork an existing direct correction. `get_latest_checkpoint` is advisory discovery state. Downstream consumers should pin `observation_id` and `result_fingerprint` and use `matches_checkpoint(...)`.

## Verification status

The v4 source is SHA-256 `0CED2851AEB13E3041D8989ADB30AB16F69D51BA34988CF5D0427EFF1ACDA952`, 30,964 bytes, and 772 lines. The ABI remains 14 methods (13 views, one write). Lint, SDK validation, strict typechecking, 54 direct tests, and three five-validator GLSim tests pass, and independent review returned `GO`.

Exact-byte deployment and the packaged semantic write/readback smoke pass on both networks:

- StudioNet: [`deployments/studionet.json`](deployments/studionet.json)
- Bradbury: [`deployments/bradbury.json`](deployments/bradbury.json), contract `0xe1e670607C75F8d5aB531DFB3000fD863Db851F4`

The Bradbury deployment finalized `AGREE / FINISHED_WITH_RETURN` with five agree votes. Its one reviewed smoke finalized with an agreed successful result, four agree votes and one validator timeout, then passed exact latest-final record, checkpoint, history, count, index, supersession, and fingerprint-gate readback.

Two superseded v3 Bradbury smoke transactions ended `UNDETERMINED / DISAGREE` with no state:

- `0xd8056970c1e7ee2ae398a8f7a5251ddfb1b2fbf6015337fa7c5b8883e8e5380c`
- `0x20e9a3cbca60ceef6a31760b2aac92c1bae7d52dfe6d9c24dd1ce07a1de6906d`

Those failures motivated the one-call minimal-claim v4 redesign and are diagnostic evidence only.

## Local verification

```powershell
genvm-lint check contracts/entity_continuity_graph.py
genvm-lint schema contracts/entity_continuity_graph.py --output abi/entity_continuity_graph.abi.json
genvm-lint typecheck contracts/entity_continuity_graph.py --strict
pytest tests/direct -q
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_glsim_5.ps1
```

## License

MIT. See `LICENSE`.
