"""Run the review agent with the Google Antigravity SDK.

Reads the prompt from PROMPT_FILE. The agent runs in read-only mode in the
current folder. Writes the review body to BODY_FILE and the verdict to the
GITHUB_OUTPUT file as "verdict=pass" or "verdict=changes-requested".

Environment:
    GEMINI_API_KEY: the Gemini API key. The SDK reads it.
    PROMPT_FILE: path to the full prompt.
    BODY_FILE: path for the review body.
    AGY_MODELS: models to try in order, separated by commas. "default" means
        the SDK default model. Empty means "default".
    AGY_ATTEMPT_SECONDS: time limit for each model. Default 360.
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path

from google.antigravity import Agent, LocalAgentConfig

VERDICTS = {"PASS": "pass", "CHANGES REQUESTED": "changes-requested"}


async def run_review(prompt: str, model: str) -> str:
    """Send the prompt to a read-only agent and return its full answer."""
    kwargs = {"model": model} if model != "default" else {}
    async with Agent(LocalAgentConfig(**kwargs)) as agent:
        response = await agent.chat(prompt)
        return await response.text()


async def run_with_fallback(prompt: str, models: list[str], seconds: float) -> tuple[str, str]:
    """Try each model in order. Return (model, answer) from the first model that answers."""
    errors = []
    for model in models:
        print(f"Trying model: {model}", flush=True)
        try:
            text = await asyncio.wait_for(run_review(prompt, model), timeout=seconds)
            return model, text
        except asyncio.TimeoutError:
            errors.append(f"{model}: no answer in {seconds:.0f} seconds")
        except Exception as error:  # The SDK raises its own error types.
            errors.append(f"{model}: {str(error)[:300]}")
        print(f"Model failed: {errors[-1]}", file=sys.stderr, flush=True)
    raise RuntimeError("All models failed:\n" + "\n".join(errors))


def parse_answer(text: str) -> tuple[str, str]:
    """Return (verdict, body) from the last JSON block in the answer."""
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not blocks:
        start = text.rfind('{"verdict"')
        if start == -1:
            raise ValueError("The answer has no JSON block.")
        blocks = [text[start:]]
    data = json.loads(blocks[-1])
    verdict = str(data["verdict"]).strip().upper()
    if verdict not in VERDICTS:
        raise ValueError(f"Unknown verdict: {verdict}")
    body = str(data["body"]).strip()
    if not body:
        raise ValueError("The review body is empty.")
    return VERDICTS[verdict], body


def main() -> int:
    prompt = Path(os.environ["PROMPT_FILE"]).read_text()
    models = [m.strip() for m in os.environ.get("AGY_MODELS", "").split(",") if m.strip()] or ["default"]
    seconds = float(os.environ.get("AGY_ATTEMPT_SECONDS", "360"))
    try:
        model, text = asyncio.run(run_with_fallback(prompt, models, seconds))
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 1
    try:
        verdict, body = parse_answer(text)
    except (ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Cannot read the review: {error}", file=sys.stderr)
        print(text[-4000:], file=sys.stderr)
        return 1
    Path(os.environ["BODY_FILE"]).write_text(body + "\n")
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"verdict={verdict}\n")
    print(f"Model: {model}. Verdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
