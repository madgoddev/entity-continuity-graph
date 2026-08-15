import json

from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded


def entity(label: str, identifier: str) -> str:
    return json.dumps(
        {
            "display_label": label,
            "jurisdiction_hint": "Exampleland",
            "public_identifier_hint": identifier,
            "descriptor_note": "Public descriptor for the integration-test graph scope",
        }
    )


def bundle(excerpt: str) -> str:
    return json.dumps(
        {
            "bundle_version": "ECG-EVIDENCE-1",
            "public_only": True,
            "privacy_attestation": "NO_PRIVATE_OR_CONFIDENTIAL_DATA",
            "documents": [
                {
                    "document_id": "doc-1",
                    "provenance_label": "PUBLIC_AUTHORITY_RECORD",
                    "capture_method": "CALLER_TRANSCRIPTION",
                    "source_title": "Public reorganization record",
                    "source_locator": "Exampleland public record 88-2026",
                    "publisher_label": "Exampleland Public Register",
                    "published_on": "2026-07-01",
                    "excerpt": excerpt,
                }
            ],
        }
    )


def result(relationship: str, direction: str) -> dict:
    return {
        "relationship": relationship,
        "succession_direction": direction,
    }


def context(classification: dict) -> dict:
    mock = {
        "nondet_exec_prompt": {
            "ENTITY_CONTINUITY_MINIMAL_CLAIM_V4": json.dumps(classification),
        },
        "eq_principle_prompt_comparative": {},
        "eq_principle_prompt_non_comparative": {},
    }
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response=mock)
    return {"validators": [validator.to_dict() for validator in validators]}


def deploy():
    factory = get_contract_factory(contract_file_path="entity_continuity_graph.py")
    contract = factory.deploy(args=[])
    assert hasattr(contract, "observe"), contract._schema
    return contract


def observe_args(
    observed_on: str,
    question: str,
    excerpt: str,
    supersedes: str = "ROOT",
    correction_reason: str = "",
) -> list[str]:
    return [
        "glsim-public-orgs-v1",
        entity("Harbor Science Association", "public id HSA-7"),
        entity("Harbor Science Foundation", "public id HSF-9"),
        observed_on,
        question,
        bundle(excerpt),
        supersedes,
        correction_reason,
    ]


def assert_five_votes(receipt: dict, expected: str) -> None:
    votes = receipt["consensus_data"]["votes"]
    assert len(votes) == 5
    assert set(votes.values()) == {expected}, receipt


def test_five_validator_same_entity_checkpoint():
    contract = deploy()
    classification = result("SAME_ENTITY", "NONE")
    receipt = contract.observe(
        args=observe_args(
            "2026-08-10",
            "Classify continuity for public research attribution only.",
            "The public record states that the association changed its registered name to the foundation without interruption.",
        )
    ).transact(transaction_context=context(classification))
    assert tx_execution_succeeded(receipt)
    assert_five_votes(receipt, "agree")
    assert contract.observation_count().call() == 1
    observation_id = contract.get_observation_id_at(args=[0]).call()
    checkpoint = contract.get_checkpoint(args=[observation_id]).call()
    assert checkpoint["claim_code"] == "SAME_ENTITY:NONE"
    assert checkpoint["decisive"] is True
    assert contract.matches_checkpoint(args=[observation_id, checkpoint["result_fingerprint"]]).call() is True


def test_five_validator_pair_history_and_successor_direction():
    contract = deploy()
    same = result("SAME_ENTITY", "NONE")
    first_receipt = contract.observe(
        args=observe_args(
            "2026-08-09",
            "First continuity checkpoint for public research attribution.",
            "The public notice describes continued programs under the foundation name during an interim period.",
        )
    ).transact(transaction_context=context(same))
    assert tx_execution_succeeded(first_receipt)
    assert_five_votes(first_receipt, "agree")
    first_id = contract.get_observation_id_at(args=[0]).call()

    successor = result("SUCCESSOR", "A_TO_B")
    second_receipt = contract.observe(
        args=observe_args(
            "2026-08-11",
            "Second continuity checkpoint for public research attribution.",
            "The later public record calls the foundation the successor to the association and states that programs transferred to it.",
            first_id,
            "Correct the earlier checkpoint using the later public record.",
        )
    ).transact(transaction_context=context(successor))
    assert tx_execution_succeeded(second_receipt)
    assert_five_votes(second_receipt, "agree")

    second_id = contract.get_observation_id_at(args=[1]).call()
    first_checkpoint = contract.get_checkpoint(args=[first_id]).call()
    page = contract.get_pair_history(args=[first_checkpoint["pair_address"], 0, 20]).call()
    assert [item["observation_id"] for item in page] == [first_id, second_id]
    latest = contract.get_latest_checkpoint(args=[first_checkpoint["pair_address"]]).call()
    assert latest["claim_code"] == "SUCCESSOR:A_TO_B"
    assert latest["observation_id"] == second_id
    assert latest["supersedes_observation_id"] == first_id
    assert contract.get_superseding_observation_id(args=[first_id]).call() == second_id


def test_five_validator_unresolved_checkpoint():
    contract = deploy()
    unresolved = result("UNRESOLVED", "NONE")
    receipt = contract.observe(
        args=observe_args(
            "2026-08-12",
            "Classify continuity where only a shared name appears publicly.",
            "The directory lists both organization names but gives no identifiers, dates, transfer language, or group relationship.",
        )
    ).transact(transaction_context=context(unresolved))
    assert tx_execution_succeeded(receipt)
    assert_five_votes(receipt, "agree")
    observation_id = contract.get_observation_id_at(args=[0]).call()
    record = contract.get_observation(args=[observation_id]).call()
    assert record["checkpoint"]["relationship"] == "UNRESOLVED"
    assert record["checkpoint"]["decisive"] is False
    assert record["classification"] == {
        "claim_code": "UNRESOLVED:NONE",
        "relationship": "UNRESOLVED",
        "succession_direction": "NONE",
    }
    assert "issue_codes" not in record
