# Decision Log

- **Hybrid decision engine:** Chose an interpretable ML risk score plus explicit business rules instead of an LLM-only classifier. Numerical RTO prediction is cheaper, faster and reproducible without an LLM.
- **LLM boundary:** Reserved AI for messy name/address quality checks such as `asdf`, `Test Order`, landmark-style Hinglish addresses and incomplete addresses. A deterministic fallback is included so the demo runs without an API key.
- **Configurable thresholds:** Put action thresholds in `config.yaml` so Operations can change policy without editing code.
- **No blanket first-order cancellation:** First-time customers are riskier, but cancellation can destroy acquisition economics. Confirmation/prepaid are safer middle options.
- **₹30 prepaid incentive:** The stated COD-vs-prepaid RTO gap implies meaningful RTO-cost savings; ₹30 is small relative to the ₹649 basket and is below the modeled expected RTO cost avoided. Exact uplift must be validated with an experiment.
- **24-hour confirmation window:** Long enough for a customer to see the message, short enough not to delay fulfillment indefinitely.
- **Random WhatsApp replies:** Clarify once rather than interpreting arbitrary text as consent.
- **No response:** For confirmation, hold/cancel after 24 hours. For prepaid nudge, do not silently convert or cancel solely because the customer ignored the offer.
- **Historical simulation:** Used September 2026, the last month represented in the supplied dataset, to answer the 'last month's orders' requirement.
- **Caution on causal claims:** Historical labels tell us what happened, but not what would have happened after a new WhatsApp intervention. Therefore avoided-RTO figures are explicitly labeled estimates based on assumptions.
