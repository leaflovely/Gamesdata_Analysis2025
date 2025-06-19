from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'message': '注册成功'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
