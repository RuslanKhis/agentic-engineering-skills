The model picks search_orders instead of get_order and passes names where IDs belong. Diagnose and fix the tool interface without changing the agent instruction.

---
Situation (from the person asking): ADK 2.8.0 project with twelve FunctionTools; two have one-line docstrings and parameters named value and data; one returns a bare string; no recorded events exist.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.