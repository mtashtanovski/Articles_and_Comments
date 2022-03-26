import json
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from rest_framework.exceptions import ValidationError

from api_v2.serializers import ArticleSerializer
from webapp.models import Article


class ArticleListView(LoginRequiredMixin, View):
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = self.serializer_class(articles, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        article_data = json.loads(request.body)
        serializer = self.serializer_class(data=article_data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return JsonResponse(data=e.detail, status=HTTPStatus.BAD_REQUEST)

        article = serializer.save(author=request.user)
        print(article.author)

        return JsonResponse(
            serializer.validated_data,
            status=HTTPStatus.CREATED
        )


class ArticleSingleObjectView(View):
    serializer_class = ArticleSerializer

    def put(self, request, *args, pk=None, **kwargs):
        article = get_object_or_404(Article, pk=pk)

        serializer = self.serializer_class(data=json.loads(request.body), instance=article)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return JsonResponse(data=e.detail, status=HTTPStatus.BAD_REQUEST)

        article = serializer.save()

        return JsonResponse(
            data=serializer.data
        )
