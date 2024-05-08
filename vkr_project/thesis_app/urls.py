from django.urls import path

from .views import SignUpView, home_view_test, reader_view, home_view, reader_view_test


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", home_view, name="home_page"),  # home page
    path('reader_view/<int:text_id>/', reader_view, name="reader_page"),
    path("home_test", home_view_test, name="home_page_test"),  # home page test
    path('reader_view_test/', reader_view_test, name="reader_page"),
]
