from openai import OpenAI
from .system_prompt import SYSTEM_PROMPT

class InterviewAgent:
    def __init__(self, api_key, resume_summary=None):
        self.client = OpenAI(api_key=api_key)

        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        # 👇 CV-ni agent-in beyninə VERİRİK
        if resume_summary:
            self.messages.append({
                "role": "system",
                "content": f"The candidate's resume summary is:\n{resume_summary}"
            })

    def ask(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer
