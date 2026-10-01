"""Generate artifacts/actual_answers.json with Gemini instead of OpenAI.

`domain_assistant.OpenAIGenerator` cannot reach Gemini: it constructs
`OpenAI(api_key=...)` with no base_url, so it always targets api.openai.com,
and it calls the Responses API, which Google's OpenAI-compatible layer answers
with 404. This runner uses the `generator` seam that `generate_actual_answers`
already exposes, so the provided system-under-evaluation file stays untouched.

The prompt, BM25 retrieval, top_k and corpus are exactly the lab defaults.

The free tier allows 20 requests per day per project per model
(GenerateRequestsPerDayPerProjectPerModel-FreeTier), and the benchmark needs
exactly one request per question. So retries are disabled and every answer is
cached to disk as it arrives; a run that runs out of quota resumes the next day
instead of starting over.
"""

import hashlib
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI, RateLimitError

from domain_assistant import generate_actual_answers

load_dotenv()

CACHE_PATH = Path("artifacts/answer_cache.json")
# The lite models answer in well under this; 300 (the OpenAIGenerator default)
# is too small for the reasoning models, which spend it before emitting text.
MAX_OUTPUT_TOKENS = 1500


class CachingGeminiGenerator:
    def __init__(self, model: str) -> None:
        self.model = model
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            base_url=os.getenv("OPENAI_BASE_URL", "").strip(),
            max_retries=0,  # a retry costs quota this run cannot spare
        )
        self.cache = (
            json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if CACHE_PATH.exists()
            else {}
        )
        self.calls = 0

    @staticmethod
    def _key(model: str, prompt: str) -> str:
        return hashlib.sha256(f"{model}\x00{prompt}".encode("utf-8")).hexdigest()[:32]

    def generate(self, prompt: str) -> str:
        key = self._key(self.model, prompt)
        if key in self.cache:
            return self.cache[key]

        response = self._call_with_retry(prompt)
        self.calls += 1
        choice = response.choices[0]
        if choice.finish_reason == "length":
            raise RuntimeError(
                f"{self.model} hit the {MAX_OUTPUT_TOKENS}-token ceiling; aborting "
                "rather than benchmarking a truncated answer."
            )
        answer = (choice.message.content or "").strip()
        if not answer:
            raise RuntimeError(f"{self.model} returned an empty answer")

        self.cache[key] = answer
        self._flush()
        return answer

    def _call_with_retry(self, prompt: str):
        """Retry transient 5xx only; a 429 means the daily quota is spent."""
        for attempt in range(6):
            try:
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_completion_tokens=MAX_OUTPUT_TOKENS,
                )
            except RateLimitError:
                raise
            except APIStatusError as exc:
                if exc.status_code < 500 or attempt == 5:
                    raise
                wait = 5 * 2**attempt
                print(
                    f"  {exc.status_code} transient; retry {attempt + 1}/5 in {wait}s",
                    flush=True,
                )
                time.sleep(wait)

    def _flush(self) -> None:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


def main() -> int:
    model = os.getenv("OPENAI_MODEL", "").strip()
    generator = CachingGeminiGenerator(model)
    cached = len(generator.cache)
    if cached:
        print(f"Resuming with {cached} cached answer(s) for {model}", flush=True)

    output = Path("artifacts/actual_answers.json")
    try:
        artifact = generate_actual_answers(
            Path("golden_dataset.json"),
            Path("data/technology_store"),
            generator=generator,
            top_k=5,
            progress=lambda message: print(message, flush=True),
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        print(f"Saving actual-answer artifact: {output}", flush=True)
        output.write_text(
            json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except RateLimitError as exc:
        quota = ""
        if "quotaValue" in str(exc):
            quota = " (daily free-tier quota exhausted)"
        print(
            f"ERROR: rate limited{quota} after {generator.calls} live call(s); "
            f"{len(generator.cache)} answer(s) are cached, so re-running tomorrow "
            "resumes where this stopped."
        )
        return 2
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 2

    print(
        f"Generated {len(artifact['answers'])} actual answers "
        f"({generator.calls} live API call(s)): {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
