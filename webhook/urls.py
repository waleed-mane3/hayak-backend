from django.urls import path

from .views import acme_webhook

urlpatterns = [
    path(
        "acme/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
        acme_webhook,
    ),
]