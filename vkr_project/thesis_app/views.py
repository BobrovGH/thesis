from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils.app_functions import analyze_polish_word, analyze_russian_word, get_info_by_table_id
from .models import Text, TranslatedSentence, TranslatedToken, WordOfDictionary
from django.http import JsonResponse
from owlready2 import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def sign_up_view(request):
    column_width = 4
    return render(request, "registration/signup.html", {"column_width": column_width})

def reader_view(request, text_id):
    text = Text.objects.get(id=text_id)
    translated_sentences = TranslatedSentence.objects.filter(text=text).order_by('paragraph')
    paragraphs = {}

    for translated_sentence in translated_sentences:
        paragraph_number = translated_sentence.paragraph
        if paragraph_number not in paragraphs:
            paragraphs[paragraph_number] = []
        sentences = TranslatedToken.objects.filter(sentence=translated_sentence).order_by('original_token_index')
        words = [(token.word_original, token.id) for token in sentences]
        paragraphs[paragraph_number].append(words)

    column_width = 10
    return render(
        request,
        "app_pages/reader_page.html",
        {
            "paragraphs": paragraphs,
            "column_width": column_width,
            "text": text,
        },
    )

def home_view(request):
    texts = Text.objects.prefetch_related('authors', 'genres').all()
    column_width = 10
    return render(
        request, 
        "app_pages/home.html", 
        {
            "texts": texts, 
            "column_width": column_width,
            "user": request.user,
        }
    )

@login_required
def dictionary_view(request):
    words = WordOfDictionary.objects.filter(user=request.user)
    return render(request, 'app_pages/dictionary.html', {'words': words})

@login_required
def delete_word(request, id):
    word = get_object_or_404(WordOfDictionary, id=id, user=request.user)
    word.delete()
    return redirect('dictionary')

@require_POST
@csrf_exempt
def add_to_dictionary(request, word_id):
    print('hello')
    if request.user.is_authenticated:
        translated_token = get_object_or_404(TranslatedToken, id=word_id)
        if WordOfDictionary.objects.filter(user=request.user, translated_token=translated_token).exists():
            return JsonResponse({'success': False, 'message': 'Word already in dictionary'}, status=400)
        else:
            WordOfDictionary.objects.create(user=request.user, translated_token=translated_token)
            return JsonResponse({'success': True, 'message': 'Word added to dictionary'})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated'}, status=403)

def get_word_analysis(request):
    word = request.GET.get('word', '')
    if not word:
        return JsonResponse([], safe=False)

    cyrillic_pattern = re.compile('[А-Яа-я]+')
    
    if cyrillic_pattern.search(word):
        data = analyze_russian_word(word)
    else:
        data = analyze_polish_word(word)
    print(data)
    return JsonResponse(data, safe=False)

def get_word_data(request, word_id):
    onto = get_ontology("populated_ontology.owl").load()
    
    word_data = get_info_by_table_id(str(word_id), onto)  # Function defined in your script
    return JsonResponse(word_data)

def yandex_form_view(request):
    return render(request, 'bases/yandex_form.html')
