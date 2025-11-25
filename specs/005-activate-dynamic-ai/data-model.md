# Data Model: Activate Dynamic AI Logic

No new persistent data models are introduced in this feature.

The primary entities are the **Internal AI Tools** (`discover_capabilities`, `submit_action_plan`), which are implemented as Python functions within the Controller.

This feature utilizes the existing data models defined in `specs/004-dynamic-command-generation/data-model.md`:
-   `CapabilityPalette`
-   `ActionPlan`
-   `ActionStep`
