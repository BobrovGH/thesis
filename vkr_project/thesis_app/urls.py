from django.urls import path

from .views import SignUpView, home_view, reader_view


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', home_view, name='home_page'), #home page
    path('reader/', reader_view, name='reader_page')
]