from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect

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
        # Now you can use the id
        thread = self.ai.create_thread()
        assistant = self.ai.get_assistant(assistant_id)
        return render(request, 'assistant/chat.html', {'assistant': assistant, 'thread': thread})
