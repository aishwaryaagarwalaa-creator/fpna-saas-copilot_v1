def sanitize_text(text: str) -> str:
    return (
        text
        .replace("\u2028", "\n")
        .replace("\u2029", "\n")
        .encode("utf-8", "ignore")
        .decode("utf-8")
    )




import time
from openai import APIConnectionError

import json
from compute import get_fpna_outputs
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()


# Initialize OpenAI client once
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




def load_rag_docs():
    def clean(text):
        return (
            text
            .replace("\u2028", "\n")
            .replace("\u2029", "\n")
            .encode("utf-8", "ignore")
            .decode("utf-8")
        )

    with open("rag/saas_glossary.md", encoding="utf-8") as f:
        glossary = clean(f.read())

    with open("rag/reporting_rules.md", encoding="utf-8") as f:
        rules = clean(f.read())

    return glossary, rules





def build_prompt(fpna_data, glossary, rules):
    prompt = f"""
You are an FP&A Narrative Copilot for a SaaS company.

Your task:
- Generate a monthly FP&A performance narrative
- Use ONLY the data provided
- Follow the reporting rules strictly
- Ground explanations in the glossary
- Do NOT fabricate causes or assumptions

====================
FINANCIAL DATA
====================
{json.dumps(fpna_data, indent=2)}

====================
FINANCE GLOSSARY
====================
{glossary}

====================
REPORTING RULES
====================
{rules}

====================
OUTPUT FORMAT
====================

1. Performance Commentary (P&L)
2. Balance Sheet Commentary
3. Leadership Summary (5–6 bullets, executive-ready)
4. Review Mode:
   - List any weak assumptions
   - List any missing data
   - Ask clarifying questions if needed
"""
    return sanitize_text(prompt)




def generate_narrative(prompt, retries=2):
    # Final safety: ensure absolutely clean unicode before API call
    safe_prompt = (
        prompt
        .replace("\u2028", "\n")
        .replace("\u2029", "\n")
        .encode("utf-8", "ignore")
        .decode("utf-8")
    )

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an FP&A Narrative Copilot."},
                    {"role": "user", "content": safe_prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content

        except APIConnectionError:
            if attempt == retries - 1:
                raise
            time.sleep(2)




    return response.choices[0].message.content


def review_narrative(narrative_text):
    review_instructions = """
You are reviewing an FP&A narrative for quality and safety.

Tasks:
- Identify any unsupported assumptions
- Flag any numerical claims not grounded in data
- Identify missing financial context
- Ask clarifying FP&A questions

Be concise and structured.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a senior FP&A reviewer."},
            {"role": "user", "content": review_instructions + "\n\n" + narrative_text}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    fpna_data = get_fpna_outputs()
    glossary, rules = load_rag_docs()
    prompt = build_prompt(fpna_data, glossary, rules)

    print("\n========== GENERATING FP&A NARRATIVE ==========\n")
    narrative = generate_narrative(prompt)
    print(narrative)

    print("\n========== REVIEW MODE ==========\n")
    review = review_narrative(narrative)
    print(review)
