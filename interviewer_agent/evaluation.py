from openai import OpenAI

EVALUATION_PROMPT = """
You are an expert interview evaluator.

Generate a Markdown report with:
- Score (0–100)
- Strengths
- Weaknesses
- Suggested Improvements
- Better Sample Answers
"""

class InterviewEvaluator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def evaluate(self, conversation_history):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": EVALUATION_PROMPT},
                {"role": "user", "content": conversation_history}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content

