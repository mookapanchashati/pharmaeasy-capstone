import json
import uuid

from datetime import datetime, timezone

def review_gate_v1(
    report,
    decision,
    reviewer_note=""
):

    allowed_decisions = {
        "approve",
        "edit",
        "reject"
    }

    if decision not in allowed_decisions:
        raise ValueError(
            "decision must be approve, edit or reject"
        )

    if decision == "approve":
        downstream_allowed = True

    else:
        downstream_allowed = False

    updated_report = report.copy()

    updated_report["review_decision"] = decision

    updated_report[
        "downstream_allowed"
    ] = downstream_allowed

    updated_report[
        "reviewer_note"
    ] = reviewer_note

    audit_entry = {

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "run_id": report.get(
            "run_id",
            str(uuid.uuid4())
        ),

        "region": report.get(
            "region",
            "Unknown"
        ),

        "decision": decision,

        "reviewer_note": reviewer_note
    }

    with open(
        "audit_log.jsonl",
        "a"
    ) as file:

        file.write(
            json.dumps(audit_entry)
            + "\n"
        )

    return updated_report


test_report = {
    "run_id": "RUN-001",
    "region": "Guntur",
    "status": "draft"
}

print("\n--- APPROVE TEST ---")

print("Before:")
print(test_report)

approved = review_gate_v1(
    test_report,
    "approve",
    "Metrics verified."
)

print("After:")
print(approved)

print("\n--- EDIT TEST ---")

print("Before:")
print(test_report)

edited = review_gate_v1(
    test_report,
    "edit",
    "Clarify the recommendation."
)

print("After:")
print(edited)

print("\n--- REJECT TEST ---")

print("Before:")
print(test_report)

rejected = review_gate_v1(
    test_report,
    "reject",
    "Requires further validation."
)

print("After:")
print(rejected)



