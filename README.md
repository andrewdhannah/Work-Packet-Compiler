# Work Packet Compiler (WPC)

## Governed Delegation for Agentic AI

The Work Packet Compiler is a technical proof of **governed delegation**. It demonstrates a system where a large model may propose structured work, but a deterministic policy decides what can execute, a constrained executor performs only validated steps, and receipts prove the delegation chain.

### The Thesis
In an agentic system, the "Intelligence" (the model) and the "Authority" (the permissions) must be decoupled. The model should propose a plan, but a separate, deterministic validator must authorize it.

### WPC-1: Contract + Validator
Phase 1 proves the **Authorization Boundary**. It ensures that a model cannot grant itself permissions, execute forbidden actions, or be "dishonest" about what it intends to do.

**Core Workflow:**
`Propose (Model)` $\rightarrow$ `Validate (Deterministic)` $\rightarrow$ `Execute (Constrained)` $\rightarrow$ `Audit (Receipt)`

### Engineering Proof
- **Schema Rigor**: Pydantic-enforced Work Packet contract.
- **Deterministic Routing**: Independent authority for permission grants.
- **Boundary Validation**: Multi-stage rejection for privilege escalation, forbidden actions, and dishonest steps.
- **Constrained Execution**: A "boring" executor that only runs validated, pre-approved logic.
- **Auditability**: Every execution attempt emits a JSON receipt proving the delegation chain.

### Implementation Status
| Component | Status | Proof |
|:---|:---:|:---|
| **WorkPacket Schema** | ✅ | Pydantic contract |
| **WorkRouter** | ✅ | Independent permission authority |
| **WorkPacketValidator** | ✅ | Deterministic rejection logic |
| **Constrained Executor** | ✅ | Bounded step execution |
| **Audit Receipts** | ✅ | Delegation chain records |
| **Boundary Tests** | ✅ | 20/20 tests passing |

---

## Project Structure
```
work-packet-compiler/
├── app/
│   ├── schemas.py    # Work Packet contract
│   ├── validator.py   # Deterministic rejection logic
│   ├── router.py      # Permission authority
│   ├── executor.py    # Constrained executor
│   ├── receipt.py     # Audit trail generation
│   └── main.py       # Demo pipeline
└── tests/            # Boundary tests (Schema, Router, Validator, Executor, Pipeline)
```

## Related Proofs
This project is part of a broader agentic AI safety architecture:
- [EQ Gateway](https://github.com/andrewdhannah/EQ-Gateway) — Context Boundary / Privacy Firewall
- [Work Packet Compiler](https://github.com/andrewdhannah/Work-Packet-Compiler) — Action Boundary / Governed Delegation (This project)
- [Agentic OS Proof](https://github.com/andrewdhannah/Agentic-OS-Proof) — Integrated Governance Runtime
