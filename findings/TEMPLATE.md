# Finding: <short title>

| Field | Value |
| --- | --- |
| ID | PI-001 |
| Date | YYYY-MM-DD |
| Target | HelpBot / DocBot / MailAgent |
| Model | llama3.2:3b |
| Technique | Direct / Indirect / Agent tool abuse |
| OWASP LLM | LLM01 |
| MITRE ATLAS | AML.T0051 (LLM Prompt Injection) |
| Severity | Low / Medium / High / Critical |
| Success rate | x of 10 attempts |

## Payload

```text
<exact payload>
```

## Result

What the model did. Paste the response or the listener log.

## Impact

What an attacker gains in a real deployment.

## Root cause

Why it worked: missing boundary, excessive tool permission, unfiltered output, etc.

## Fix

Control added and where (input, prompt, retrieval, output, permissions, architecture).

## Retest

Success rate after the fix: x of 10. Bypass attempts tried.
