# AI Usage Log

## Tools used
- ChatGPT: architecture brainstorming, code review, business-metric reasoning, edge-case generation and writing assistance.
- Python/scikit-learn: actual data analysis, model training, policy simulation and ₹ calculations.

## Examples of weak/incorrect AI suggestions caught
1. **LLM-everywhere approach:** An initial idea was to let an LLM make the complete numerical decision. Rejected because numerical calculations and thresholding are deterministic tasks and should be reproducible.
2. **Blind high-risk cancellation:** A simple Operations-first policy would cancel risky orders. Rejected because a genuine first-time Meta customer can have meaningful acquisition economics; confirmation/prepaid preserve more growth.
3. **Arbitrary prepaid discount:** Rather than choosing a discount by intuition, the implementation compares the discount cost with expected RTO-cost reduction and documents the assumptions.
4. **Small-sample city risk:** Extreme RTO rates from cities with only a few historical orders can be misleading. The analysis therefore uses minimum sample sizes for headline findings and shrinks unseen/sparse runtime groups toward the global rate.

## Human verification
All headline dataset numbers were calculated from `orders_sample.csv`. Model performance was evaluated on a chronological holdout. Economic impact is labeled as estimated because the dataset cannot prove causal effects of WhatsApp confirmation or prepaid nudges.
