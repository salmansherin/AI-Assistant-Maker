from django.shortcuts import render
from openai import OpenAI


def dashboard(request):
    client = OpenAI()
    assistants = client.beta.assistants.list(
        order="desc",
        limit=20,
    )
    return render(request, 'assistant/dashboard.html', {'assistants': assistants})
