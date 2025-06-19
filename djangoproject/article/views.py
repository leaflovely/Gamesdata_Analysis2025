from rest_framework.response import Response
from .serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Article
from rest_framework import permissions

class GetArticleAPIView(APIView):
    def get(self, request):
        # 处理GET请求
        articles = Article.objects.all()  # queryset数据类型转成JSON数据类型
        serializer = ArticleSerializer(articles, many=True)
        return Response({'code': 200, 'data': serializer.data})


# 搜索文章视图类
class SearchArticleAPIView(APIView):
    def post(self, request):
        print(request.data.get('question'))
        # 处理POST请求
        articles = Article.objects.filter(question__icontains=request.data.get('question'))
        serializer = ArticleSerializer(articles, many=True)
        return Response({'code': 200, "data": serializer.data})


class PublishArticleAPIView(APIView):
    # 校验前端token是正确
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'message':'发布成功'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)