from django.urls import path

from .views import SignUpView, my_view, reader_view


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', my_view, name='my_page'), #home page
    path('reader/', reader_view, name='reader')
]