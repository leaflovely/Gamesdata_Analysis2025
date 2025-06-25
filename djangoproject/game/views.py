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


class SearchGameAPIView(APIView):
    def post(self, request):
        game = Game.objects.filter(chinese_name__icontains=request.data['question'])
        serializer = GameSerializer(game, many=True)
        return Response({'code': 200, 'data': serializer.data})