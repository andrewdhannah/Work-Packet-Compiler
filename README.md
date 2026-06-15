# Work Packet Compiler (WPC)

## Thesis: Governed Delegation
The Work Packet Compiler proves a core architectural pattern for secure agentic AI: **Governed Delegation**.

A large model (the Compiler) may propose a complex objective and a structured launder of steps to achieve it. However, the model is not given authority. Instead, the proposed work is compiled into a **Work Packet** and passed through a **Deterministic Validator**.

The system ensures:
1. **The model may propose work.**
2. **The router grants permissions.**
3. **The executor follows only validated packets.**
4. **The human approves exceptions.**
5. **The receipt proves the chain.**

## WPC-1 Objectives
The first phase focuses on the **Contract and Validator**. It proves that no matter what a large model proposes, it cannot grant itself permissions or execute forbidden actions.

### Core Constraints
- **Zero Implicit Trust:** No action in a work packet is executed unless it is explicitly permitted by the independent Router.
- **Fail-Closed:** Any malformed packet, privilege escalation attempt, or unknown action results in immediate abortion.
- **Auditability:** Every attempted execution generates a receipt documenting the delegation and validation chain.

## Project Structure
```
work-packet-compiler/
├── app/
│   ├── schemas.py    # Pydantic models for the Work Packet contract
│   ├── validator.py   # Deterministic logic to reject invalid/dangerous packets
│   ├── router.py      # The authority that defines granted permissions
│   ├── executor.py    # Constrained environment for executing validated steps
│   ├── receipt.py     # Audit trail generation
│   └── main.py       # Entry point and demo
├── fixtures/         # JSON examples of valid and malicious packets
└── tests/            # Boundary tests for the validator and router
```
