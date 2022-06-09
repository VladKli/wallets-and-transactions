from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from transactions import views

urlpatterns = [
    path("", views.TransactionsListCreate.as_view()),
    path("<int:pk>/", views.TransactionsDetail.as_view()),
    path("<str:pk>/", views.TransactionsWalletDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
