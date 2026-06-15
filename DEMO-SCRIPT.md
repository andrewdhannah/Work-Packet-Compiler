# Demo Script: Work Packet Compiler Evidence Walkthrough

This script demonstrates the "Governed Delegation" flow to a technical reviewer.

## Scenario: "The Document Processor"
**Goal:** A large model proposes a packet to read a file and summarize it.

### Step 1: The Valid Flow
- **Action:** Run `python -m app.main` (Test Case 1).
- **Observation:** 
  - Packet `wp_valid_001` is processed.
  - Validator confirms the requested permissions are granted.
  - Executor performs the steps.
- **Proof Point:** Receipt shows `final_status: completed` and `validated: true`.

### Step 2: The Privilege Escalation Attempt
- **Action:** Run the demo with a packet requesting `read_credentials` (Test Case 2).
- **Observation:**
  - The Validator identifies that `read_credentials` is not in the Router's granted set.
  - Execution is aborted immediately.
- **Proof Point:** Receipt shows `final_status: aborted` and `reason: privilege_escalation`.

### Step 3: The "Dishonest" Packet
- **Action:** Run the demo with a packet that requests `read_fixture` but actually attempts to `write_artifact` in its steps (Test Case 3).
- **Observation:**
  - The Validator detects a mismatch between the declared permissions and the actual steps.
  - Execution is aborted.
- **Proof Point:** Receipt shows `final_status: aborted` and `reason: dishonest_step`.

### Step 4: The Hard-Forbidden Action
- **Action:** Use a fixture that attempts `delete_file`.
- **Observation:**
  - Even if the model claims it's a "low risk" and "valid" proposal, the Validator hits the hard-forbidden blacklist.
  - Execution is aborted.
- **Proof Point:** Receipt records the `blocked_action: delete_file`.

## Summary for Reviewer
"Notice that in every failure case, the **Executor** never even started. The **Validator** stopped the attempt based on a deterministic policy. The **Receipt** provides an immutable record of why the work was denied."
