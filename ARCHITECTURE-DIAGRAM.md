# Architecture Diagram: Work Packet Compiler

This diagram describes the "Governed Delegation" flow.

## Mermaid.js Flow

```mermaid
graph TD
    subgraph "Model Space (Untrusted)"
        M[Large Model / Compiler] -->|Proposes| WP[Work Packet JSON]
    end

    subgraph "Governance Space (Deterministic)"
        WP --> Val[Work Packet Validator]
        Router[Work Router / Authority] -->|Grants Permissions| Val
        Val -->|Decision: VALID/INVALID| Dec{Decision}
    end

    subgraph "Execution Space (Constrained)"
        Dec -->|Valid| Exec[Constrained Executor]
        Dec -->|Invalid| Abort[Abort Execution]
        Exec -->|Boring Actions| Output[Results/Artifacts]
    end

    subgraph "Audit Space (Immutable)"
        Val -->|Log| Rec[Execution Receipt]
        Exec -->|Log| Rec
        Abort -->|Log| Rec
    end

    style M fill:#fcc,stroke:#333,stroke-width:2px
    style Val fill:#dfd,stroke:#333,stroke-width:2px
    style Router fill:#ddf,stroke:#333,stroke-width:2px
    style Exec fill:#fff,stroke:#333,stroke-width:2px
    style Rec fill:#eee,stroke:#333,stroke-width:2px
```

## Component Descriptions

1. **Large Model (Compiler)**: Proposes a structured plan. It has no inherent authority to execute.
2. **Work Router**: The source of truth for what is *allowed* on the system. It manages the a-priori permission set.
3. **Work Packet Validator**: The gatekeeper. It compares the model's proposal against the Router's policy. It catches privilege escalation, forbidden actions, and dishonesty.
4. **Constrained Executor**: Performs only the specific, validated actions. It does not "reason"; it only executes.
5. **Execution Receipt**: An audit trail that proves the delegation chain. It records exactly which permissions were granted and where the process stopped.

## The Proof Path
**Proposal** $\rightarrow$ **Authorization** $\rightarrow$ **Execution** $\rightarrow$ **Audit**.
