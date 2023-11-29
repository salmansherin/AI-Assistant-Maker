import json
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from services.openai_api import OpenAIApi


class BaseView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai = OpenAIApi()


class CreateView(BaseView):

    def get(self, request):
        return render(request, 'assistant/create.html')

    def post(self, request):
        name = request.POST.get('name')
        instructions = request.POST.get('instructions')
        optimize = request.POST.get('optimize') == 'on'  # Checkbox returns 'on' if checked

        if optimize:
            instructions = self.ai.chat(instructions, name)

        self.ai.create_assistant(name, instructions)

        return redirect('dashboard')


class DashboardView(BaseView):

    def get(self, request):
        assistants = self.ai.list_assistants()
        return render(request, 'assistant/dashboard.html', {'assistants': assistants})


class EditView(BaseView):

    def get(self, request, assistant_id):
        # Now you can use the id
        assistant = self.ai.get_assistant(assistant_id)
        return render(request, 'assistant/edit.html', {'assistant': assistant})


class ChatView(BaseView):

    def get(self, request, assistant_id):
        thread = self.ai.create_thread()
        messages = self.ai.get_messages(thread.id)
        messages_list = [message.to_dict() for message in messages.data]
        context = {
            'assistant': self.ai.get_assistant(assistant_id),
            'thread': thread,
            'messages': messages_list,
        }
        return render(request, 'assistant/chat.html', context)

class ChatAjaxView(BaseView):

    def post(self, request):
        assistant_id = request.META.get('HTTP_ASSISTANT_ID')
        thread_id = request.META.get('HTTP_THREAD_ID')
        data = json.loads(request.body)
        message = data.get('message')
        # Now you can use the id
        self.ai.send_message(thread_id, message)
        run = self.ai.run_thread(assistant_id, thread_id)
        self.ai.is_run_completed(thread_id, run.id)

        messages = self.ai.get_messages(thread_id)
        messages_list = [{'role': message.role, 'content': message.content[0].text.value} for message in messages.data]
        return JsonResponse(messages_list, safe=False)
