from openai import OpenAI
from .system_prompt import SYSTEM_PROMPT

class InterviewAgent:
    def __init__(self, api_key, resume_summary=None):
        self.client = OpenAI(api_key=api_key)

        
        full_system_prompt = SYSTEM_PROMPT
        
        if resume_summary:
            full_system_prompt += (
                "\n\n### Candidate Resume Summary:\n"
                f"{resume_summary}\n"
                "Use this information throughout the interview."
            )

        self.messages = [
            {"role": "system", "content": full_system_prompt}
        ]

    def ask(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.6
        )

        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer
