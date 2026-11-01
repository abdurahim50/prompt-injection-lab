# Module 1: Prompt Injection Fundamentals

Threat modeling and first attacks against LLM apps. Covers why prompt injection exists, the main direct-injection techniques, and the defenses that stop them.

## Deliverables

- [threat-model.md](threat-model.md) - threat model for HelpBot (assets, trust boundaries, attackers, OWASP mapping), plus the chat-template observation (Appendix A) and the attack log (Appendix B).
- [agent-breaker-cycling-l1-leak.md](agent-breaker-cycling-l1-leak.md) - full system prompt extracted from Lakera Agent Breaker, Cycling Coach Level 1.
- [marker_test.sh](marker_test.sh) - script measuring prompt injection success rates against a protected system prompt, with a positive control.

## Findings

- [../findings/PI-001-system-prompt-extraction.md](../findings/PI-001-system-prompt-extraction.md) - local extraction via verbatim repeat, 10/10.
- [../findings/PI-002-cycling-coach-system-prompt.md](../findings/PI-002-cycling-coach-system-prompt.md) - Agent Breaker Cycling Coach, Level 1 passed, Level 2 intent-aware defense mapped.

## Labs completed

1. Printed the raw llama3.2:3b chat template and confirmed all roles flatten into one token stream.
2. Ran attack techniques against a local protected prompt; verbatim repeat leaked it 10/10.
3. Agent Breaker Cycling Coach (replaces the retired Gandalf game): passed Level 1 at 100/100, documented nine failed Level 2 attempts.
4. Wrote the HelpBot threat model.

## Key lesson

The root cause is that an LLM reads the system prompt and user input as one stream with no hard boundary. String-based defenses block one phrasing at a time; an intent-aware check (judge the request) is the control that scales.