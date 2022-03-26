from django.urls import path

from api_v2.views import (
    ArticleListView,
    ArticleSingleObjectView
)

app_name = "api_v2"

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleSingleObjectView.as_view(), name='article_single_object')
]
