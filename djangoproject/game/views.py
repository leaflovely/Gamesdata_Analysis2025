from rest_framework.response import Response
from .serializers import GameSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Game
from rest_framework import permissions

class GetGameAPIView(APIView):
    def get(self, request):
        # 处理GET请求
        game = Game.objects.all()  # queryset数据类型转成JSON数据类型
        serializer = GameSerializer(game, many=True)
        return Response({'code': 200, 'data': serializer.data})


# 搜索游戏视图类
class SearchGameAPIView(APIView):
    def post(self, request):
        print(request.data.get('name'))
        # 处理POST请求
        game = Game.objects.filter(name__icontains=request.data.get('name'))
        serializer = GameSerializer(game, many=True)
        return Response({'code': 200, "data": serializer.data})

