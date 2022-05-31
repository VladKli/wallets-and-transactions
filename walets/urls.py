from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from walets import views

urlpatterns = [
    path("", views.WalletsList.as_view()),
    path("<slug:name>/", views.WalletsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
