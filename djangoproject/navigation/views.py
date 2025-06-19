from rest_framework.response import Response
from .serializers import NavigationSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Navigation


class GetNavigationAPIView(APIView):
    def get(self, request):
        navigation = Navigation.objects.all()
        serializer = NavigationSerializer(navigation, many=True)
        return Response({'code': 200, 'data': serializer.data})
