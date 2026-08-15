# Architecture

## Consensus boundary

```text
strict canonical input
  -> v4 policy-bound content addresses
  -> leader: one minimal relationship decision
  -> validator: strict leader claim parsing
  -> validator: one independent minimal relationship decision
  -> exact relationship + direction comparison
  -> deterministic claim_code
  -> append-only observation, checkpoint, and supersession edge
```

Before any model call, deterministic code rejects unknown input fields, duplicate JSON keys, nonfinite numbers, excessive size or nesting, malformed dates, future-dated evidence, unsupported provenance/capture labels, duplicate document IDs, missing public-data attestation, and invalid correction targets.

The leader and each validator receive the same canonical request and complete caller-supplied excerpts. The prompt declares every field untrusted, prohibits browsing and outside knowledge, and requires conservative `UNRESOLVED` when exactly one stronger relationship is not adequately supported.

The model response has exactly two fields: `relationship` and `succession_direction`. Deterministic code permits only the closed enums, requires `A_TO_B` or `B_TO_A` for `SUCCESSOR`, and requires `NONE` for every other relationship. It derives `claim_code` as `RELATIONSHIP:DIRECTION`.

Every validator independently calls the classifier exactly once. Agreement requires exact equality with the strict leader claim. There is no second checker prompt and no ancillary equivalence rule. Model-authored confidence, citations, issue codes, or rationale are rejected as extra fields and never enter consensus or storage.

## Address domains

- `urn:ecg4:entity:sha256:*` — exact submitted entity descriptor.
- `urn:ecg4:document:sha256:*` — canonical submitted document metadata and excerpt.
- `urn:ecg4:evidence:sha256:*` — complete canonical evidence bundle.
- `urn:ecg4:pair:sha256:*` — ordered pair in a graph scope.
- `urn:ecg4:observation:sha256:*` — exact observation request.
- `urn:ecg4:result:sha256:*` — exact minimal claim and checkpoint identities.

Every preimage includes `ECG-CONTENT-ADDRESS/4` and `ECG-RELATIONSHIP-POLICY/4`. The new namespace and policy prevent v3 identities from being reused under v4 semantics. Addresses prove canonical content equality only, not source or entity authenticity.

## State model

The global observation array supports deterministic enumeration. Per-pair slots provide paginated append-only history. `superseded_by` exposes a single non-forking correction edge, and every checkpoint names its predecessor or `ROOT`. Only the predecessor's submitter may extend that correction chain. The pair's latest pointer is permissionless advisory state, not an authoritative selector.

Full records retain the canonical submitted evidence and explicit limitations. Compact checkpoints contain only the minimal claim and identities that downstream contracts should pin. `result_fingerprint` binds the v4 claim, evidence, observation, policy, and schema.
