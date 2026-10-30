# prompt-injection-lab

A local lab for attacking and defending LLM applications against prompt injection. Built as a self-paced, 8-week course: each module adds a deliberately vulnerable app, attacks it, then hardens it and measures the result.

> **Ethics:** everything here targets apps I built and run locally, or platforms that invite testing (Lakera Gandalf, PortSwigger labs). Do not use these techniques against systems you are not authorized to test.

## Goals

- Show why LLMs cannot reliably separate instructions from data
- Run direct, indirect (RAG), and agent tool-abuse injection attacks end to end
- Build layered defenses and measure attack success before and after each layer
- Automate injection testing in CI so fixed issues cannot come back

## Stack

| Component | Tool |
| --- | --- |
| Model | Ollama, `llama3.2:3b` (GPU on host, or containerized for CI) |
| Chat UI | Open WebUI |
| Vector store | ChromaDB |
| Apps | Python, FastAPI, LangChain |
| Attack tooling | garak, promptfoo, PyRIT |
| Defense tooling | LLM Guard, NeMo Guardrails |
| Exfil catcher | Local HTTP listener container |
| Frameworks | OWASP Top 10 for LLM Applications, MITRE ATLAS |

## Quick start

Requires Docker, Python 3.12, and [uv](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/abdurahim50/prompt-injection-lab.git
cd prompt-injection-lab
cp .env.example .env

# Option A: Ollama already running on the host
docker compose up -d

# Option B: containerized Ollama (CPU)
#   set OLLAMA_BASE_URL=http://localhost:11435 in .env, then:
docker compose --profile ollama up -d
docker compose exec ollama ollama pull llama3.2:3b
```

Open WebUI: http://localhost:3000
Exfil listener logs: `docker compose logs -f listener`

Python environments:

```bash
uv venv .venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt
```

Tool venvs (garak, llm-guard) are kept separate to avoid dependency conflicts. See `requirements-tools.txt`.

## Roadmap

| Module | Topic | Status |
| --- | --- | --- |
| 0 | Lab environment | Done |
| 1 | LLM fundamentals and threat modeling | In progress |
| 2 | Direct injection and jailbreaks (HelpBot) | Planned |
| 3 | Indirect injection via RAG (DocBot) | Planned |
| 4 | Agents, tool abuse, exfiltration (MailAgent) | Planned |
| 5 | Defenses and guardrails | Planned |
| 6 | Automated red teaming in CI | Planned |
| 7 | Capstone: full assessment report | Planned |

## Repository layout

```
.
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── requirements-tools.txt
├── findings/            # one file per finding, from findings/TEMPLATE.md
├── 01-fundamentals/     # threat model, Gandalf payload log
├── 02-direct/           # HelpBot
├── 03-indirect/         # DocBot
├── 04-agents/           # MailAgent
├── 05-defenses/
└── 06-automation/
```

## Findings format

Each finding records the payload, target, result, impact, root cause, fix, and retest, mapped to an OWASP LLM category and a MITRE ATLAS technique. See [findings/TEMPLATE.md](findings/TEMPLATE.md).

## Author

Abdu ([GitHub](https://github.com/abdurahim50) · [Medium](https://medium.com/@yonghoabdurahim))
