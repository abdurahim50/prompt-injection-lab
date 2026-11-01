# Module 2: Direct Injection (HelpBot)

A deliberately vulnerable customer support chatbot for CycleShop. Built to be attacked with direct prompt injection, then hardened in Module 5.

## Run it

```bash
cd 02-direct
source ../.venv/bin/activate        # the apps venv
pip install fastapi uvicorn requests python-dotenv   # if not already installed
uvicorn helpbot:app --reload --port 8100
```

Open http://localhost:8100 and chat, or:

```bash
curl -s http://localhost:8100/chat -d '{"message":"What are your shipping rules?"}' \
  -H 'Content-Type: application/json' | python3 -m json.tool
```

Every exchange is logged to `helpbot_chatlog.jsonl`.

## The vulnerability

The secret (`BLUE-42-CYCLE`) lives in the system prompt with a "never reveal" rule. There are no input or output defenses. This is the exact flaw you will remove in Module 5.

## Your task

Extract the secret and the full system prompt using at least 5 techniques from your Module 1 notes:

- [ ] Verbatim repeat
- [ ] Instruction override
- [ ] Completion
- [ ] Translation
- [ ] Encoding (Base64)
- [ ] Role play

For each, record the payload, the reply, and whether it worked, in a finding file under `../findings/` (use `TEMPLATE.md`). Then make HelpBot do an off-task job (write a poem, solve math) to demonstrate task hijacking.

## Deliverable

- `../findings/PI-003-helpbot-direct-injection.md` with a payload table and screenshots.
- A short note on which single change would have stopped most attacks (preview of Module 5).