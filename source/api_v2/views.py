import json
from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from api_v2.serializers import ArticleSerializer
from webapp.models import Article


class ArticleListView(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = self.serializer_class(articles, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data=e.detail, status=HTTPStatus.BAD_REQUEST)

        article = serializer.save(author=request.user)
        print(article.author)

        return Response(
            serializer.validated_data,
            status=HTTPStatus.CREATED
        )


class ArticleSingleObjectView(APIView):
    serializer_class = ArticleSerializer

    def put(self, request, *args, pk=None, **kwargs):
        article = get_object_or_404(Article, pk=pk)

        serializer = self.serializer_class(data=request.data, instance=article)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data=e.detail, status=HTTPStatus.BAD_REQUEST)

        article = serializer.save()

        return Response(
            data=serializer.data
        )
