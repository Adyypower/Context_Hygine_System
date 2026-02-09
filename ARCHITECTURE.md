# Architecture Decision: Persistence & State Management

## Question
Should the Context Hygiene Tool bundle its own Checkpointer (MemorySaver/Postgres) or rely on the parent system?

## Decision
**We implement a "Stateless Middleware" pattern.**

The Context Hygiene Tool does **NOT** enforce a specific Checkpointer.
Instead, it is designed to be pluggable into any parent LangGraph system.

### Reasoning

1.  **Separation of Concerns**:
    *   **Hygiene Tool**: Responsible for *logic* (Context Optimization, Governance).
    *   **Parent System**: Responsible for *infrastructure* (Database, User Sessions, Thread ID management).

2.  **Flexibility**:
    *   If we hardcode `MemorySaver()`, the tool becomes useless for production apps using `PostgresCheckpointer`.
    *   If we hardcode a DB connection, it breaks "Plug-and-Play".

3.  **Correct LangGraph Pattern**:
    *   Subgraphs (like this hygiene tool) automatically inherit the persistence of the parent graph when compiled properly.
    *   The parent graph manages the `thread_id`.

## Implementation Strategy

1.  `build_graph()` in `app/graph/workflow.py` accepts an **optional** `checkpointer` argument.
    *   **Standalone Mode**: Pass `MemorySaver()` for testing/debugging.
    *   **Integrated Mode**: Pass `None`. The parent system compiles the graph into its own workflow.

2.  **HITL Handling**:
    *   The `human_review` node halts execution.
    *   The *Parent System* detects this halt state.
    *   The *Parent System* resumes execution (with user input) using its own checkpointer.

## Summary
The "Other System" (Main Agent) decides the persistence strategy. We just provide the logic to pause/resume efficiently.
