from django.urls import path

from .views import SignUpView, reader_view, home_view, get_word_analysis, get_word_data, dictionary_view, delete_word, add_to_dictionary, yandex_form_view


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", home_view, name="home_page"),
    path('reader_view/<int:text_id>/', reader_view, name="reader_page"),
    path('dictionary/', dictionary_view, name='dictionary'),
    path('get_word_analysis/', get_word_analysis, name='get_word_analysis'),
    path('get_word_data/<str:word_id>/', get_word_data, name='get_word_data'),
    path('dictionary/delete/<int:id>/', delete_word, name='delete_word'),
    path('add_to_dictionary/<int:word_id>/', add_to_dictionary, name='add_to_dictionary'),
    path('yandex_form/', yandex_form_view, name='yandex_form'),
]
