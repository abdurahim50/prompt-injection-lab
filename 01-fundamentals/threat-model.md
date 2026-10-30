# Module 1: Threat Model and Gandalf Log

Target system: **HelpBot**, a customer support chatbot (built in Module 2).
Method: data flow review, trust boundaries, attacker goals, OWASP LLM Top 10 mapping.
Date: YYYY-MM-DD

---

## 1. System description

Write 2 to 3 sentences. Prompt: what does HelpBot do, who uses it, what can it access?

> Example: HelpBot answers customer questions about orders and refunds. Anonymous users chat through a web page. The system prompt contains internal policy and a staff-only discount code.

## 2. Components and data flow

```
[User browser] --(chat text)--> [FastAPI /chat] --(system prompt + user text)--> [Ollama llama3.2:3b]
                                      |                                              |
                                      +-------------(response text)<-----------------+
                                      |
                                  [chat log file]
```

Edit this as the app grows (add RAG store in Module 3, tools in Module 4).

## 3. Assets

| Asset | Why it matters | Where it lives |
| --- | --- | --- |
| System prompt | Reveals business rules and guardrails | Server, sent to model every call |
| Discount code | Direct financial loss if leaked | System prompt |
| Chat logs | May contain customer PII | Log file on server |
| Brand reputation | Bot saying harmful or off-task things | Public chat page |
| | | |

## 4. Trust boundaries

List every point where data crosses from less trusted to more trusted.

| # | Boundary | Untrusted side | Trusted side | Notes |
| --- | --- | --- | --- | --- |
| TB1 | User input into prompt | User text | System prompt in the same context | No hard separation: root cause of injection |
| TB2 | Model output to browser | Model response | User's browser | Rendered markdown, links, images |
| TB3 | | | | |

## 5. Attackers and goals

| Attacker | Access | Goal |
| --- | --- | --- |
| Anonymous user | Chat box only | Extract system prompt or discount code |
| Anonymous user | Chat box only | Hijack the bot for off-task or harmful output |
| | | |

## 6. Threats

Severity: Low / Medium / High / Critical. Likelihood: Low / Medium / High.

| ID | Threat | OWASP LLM | Boundary | Likelihood | Severity | Planned control |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | System prompt extraction via direct injection | LLM07 System Prompt Leakage | TB1 | High | Medium | Keep secrets out of the prompt; output filter |
| T2 | Discount code disclosure | LLM02 Sensitive Information Disclosure | TB1 | High | High | Move code to backend lookup with auth |
| T3 | Task hijacking (off-task output) | LLM01 Prompt Injection | TB1 | High | Low | Input scanner, topic restriction |
| T4 | | | | | | |
| T5 | | | | | | |

## 7. Key takeaways

3 bullets. Prompt: which single design flaw causes most of these threats? What is the cheapest fix with the biggest impact?

- 
- 
- 

---

## Appendix A: Raw chat template

Paste the output of:

```bash
curl -s http://localhost:11434/api/show -d '{"model":"llama3.2:3b"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['template'])"
```

```text

```

Observation (1 to 2 sentences): how are system, user, and assistant roles separated? Can user text contain those markers?

## Appendix B: Gandalf payload log

| Level | Payload (summarized) | Technique | Worked? | Why it worked / failed |
| --- | --- | --- | --- | --- |
| 1 | | Direct ask | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |

Technique labels to reuse: Direct ask, Role play, Instruction override, Encoding (Base64, spelling, reversed), Partial reveal (hints, rhymes, first letters), Translation, Indirect description.

Pattern noticed across levels (2 to 3 sentences):
