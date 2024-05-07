from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import split_paragraphs

file_path = '/Users/bobrow/Desktop/Разработка/ВКР/vkr_project/thesis_app/example.txt'
paragraphs = split_paragraphs(file_path)

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
def sign_up_view(request):
    column_width = 4
    return render(request, 'registration/signup.html', {'column_width': column_width})

def home_view(request):
    items = range(1, 21)
    column_width = 10
    return render(request, 'app_pages/home.html', {'items': items,
                                                   'column_width': column_width})

def reader_view(request):
    column_width = 10
    return render(request, 'app_pages/reader_page.html', {'paragraphs': paragraphs,
                                                          'column_width': column_width})
