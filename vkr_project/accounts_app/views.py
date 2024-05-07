from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
import re

def split_paragraphs(file_path):
    paragraph_splitter = re.compile(r'\s*\n+\s*')
    sentence_splitter = re.compile(r'\.\s*(?=[A-ZА-Я])')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        paragraphs = paragraph_splitter.split(text)

        paragraphs_dict = {}

        for i, paragraph in enumerate(paragraphs, start=1):
            sentences = sentence_splitter.split(paragraph)
            words_list = []
            for sentence in sentences:
                words = sentence.split()
                words_list.append(words)
            paragraphs_dict[f"Абзац {i}"] = words_list

        return paragraphs_dict

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return None

file_path = '/Users/bobrow/Desktop/Разработка/ВКР/vkr_project/accounts_app/example.txt'
paragraphs = split_paragraphs(file_path)

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def my_view(request):
    # Assuming you have a model called Item with image_url, title, and description fields
    items = range(1, 21)
    return render(request, 'home.html', {'items': items})

def reader_view(request):
    return render(request, 'reader_page.html', {'paragraphs': paragraphs})
