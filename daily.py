import os, requests, datetime

PROMPT = """Jesteś botem propagandowym fikcyjnego serwera discord RPGOWNIA. 
Na tym serwerze odgrywa się roleplay gdzie rządzi Partia RPGOWNI a przeciw niej nastawiona jest Opozycja. 
Hasla mają być dość krótkie, a przy tym chwytliwe aby oddały maksimum propagandy. 
Wygeneruj hasło propagandowe dla RPGOWNI na rozpoczęcie dnia."""

r = requests.post(
    "https://api.openai.com/v1/responses",
    headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
             "Content-Type": "application/json"},
    json={"model": "gpt-6-luna",
          "reasoning": {"effort": "low"},  # cheap & fast; it's a joke message, not a thesis
          "input": PROMPT},
    timeout=120,
)
r.raise_for_status()

# Pull the text out of the Responses API output (skips reasoning items)
text = "".join(
    part["text"]
    for item in r.json()["output"] if item["type"] == "message"
    for part in item["content"] if part["type"] == "output_text"
).strip()

resp = requests.post(os.environ["DISCORD_WEBHOOK"], json={"content": text[:2000]}, timeout=30)
resp.raise_for_status()