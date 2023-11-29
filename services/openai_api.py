from openai import OpenAI


class OpenAIApi:
    def __init__(self):
        self.ai = OpenAI()

    def chat(self, prompt, name):
        system_message = "You are a helpful assistant."
        user_message = "Elaborate on the following text as an instruction for an A.I assistant."
        user_message += "\n\nAssistant Name:" + name
        user_message += "\n\nInput Instructions:" + prompt
        user_message += "\n\nOutput Instructions:"
        completion = self.ai.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
        )

        return completion.choices[0].message.content

    def create_assistant(self, name, instructions):
        assistant = self.ai.beta.assistants.create(name=name, instructions=instructions, model='gpt-4')
        return assistant

    def list_assistants(self):
        assistants = self.ai.beta.assistants.list()
        return assistants

    def get_assistant(self, assistant_id):
        assistant = self.ai.beta.assistants.retrieve(assistant_id)
        return assistant

    def get_messages(self, thread_id):
        messages = self.ai.beta.threads.messages.list(thread_id=thread_id)
        return messages

    def create_thread(self):
        thread = self.ai.beta.threads.create()
        return thread

    def send_message(self, thread_id, message):
        self.ai.beta.threads.messages.create(thread_id=thread_id, content=message, role="user")

    def run_thread(self, assistant_id, thread_id):
        return self.ai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    def is_run_completed(self, thread_id, run_id):
        while True:
            run = self.ai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if run.status == "completed":
                break
