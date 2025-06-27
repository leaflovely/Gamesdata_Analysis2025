from rest_framework.response import Response
from .serializers import GameSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Game
from rest_framework import permissions
import json
from django.db.models import Q


# 在RatingAPIView中添加对review_user字段的更新逻辑
class RatingAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        rating = request.data.get('rating')
        gameId = request.data.get('gameId')

        try:
            game = Game.objects.get(id=gameId)
            # 确保review_user字段有默认值'[]'
            review_user = json.loads(game.review_user) if game.review_user else {}

            # 更新用户评分
            review_user[username] = rating
            game.review_user = json.dumps(review_user)

            # 重新计算用户评分统计数据
            ratings = [float(r) for r in review_user.values()]
            if ratings:
                game.user_reviews_number = len(ratings)
                game.user_score = sum(ratings) / len(ratings)
                # 计算好评率等（示例逻辑，可根据实际需求调整）
                positive = sum(1 for r in ratings if r >= 7)
                negative = sum(1 for r in ratings if r < 4)
                mixed = len(ratings) - positive - negative

                game.user_positive = round((positive / len(ratings)) * 100)
                game.user_negative = round((negative / len(ratings)) * 100)
                game.user_mixed = round((mixed / len(ratings)) * 100)

            game.save()
            return Response({'code': 200, 'message': '评分成功'})
        except Game.DoesNotExist:
            return Response({'code': 404, 'message': '游戏不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'code': 500, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetGameAPIView(APIView):
    def get(self, request):
        # 获取页码参数，默认为第一页
        page = int(request.query_params.get('page', 1))
        page_size = 24  # 每页返回24条数据
        offset = (page - 1) * page_size
        limit = offset + page_size

        # 查询数据库并分页
        games = Game.objects.all()[offset:limit]
        serializer = GameSerializer(games, many=True)
        return Response({'code': 200, 'data': serializer.data})


class SearchGameAPIView(APIView):
    def post(self, request):
        game = Game.objects.filter(chinese_name__icontains=request.data['question'])
        serializer = GameSerializer(game, many=True)
        return Response({'code': 200, 'data': serializer.data})


class FilterGameAPIView(APIView):
    def post(self, request):
        print("收到筛选请求:", request.data)
        platforms = request.data.get('platforms', [])
        genres = request.data.get('genres', [])
        page = int(request.data.get('page', 1))
        page_size = int(request.data.get('pageSize', 24))

        # 初始查询集
        queryset = Game.objects.all()

        try:
            # 平台筛选 - 使用精确匹配而不是模糊匹配
            if platforms:
                platform_conditions = Q()
                for platform in platforms:
                    # 处理平台名称中可能包含的特殊字符
                    platform = platform.replace('-', ',').strip()
                    platform_conditions |= Q(platform__contains=platform)
                queryset = queryset.filter(platform_conditions)
                print(f"应用平台筛选后的结果数: {queryset.count()}")

            # 游戏类型筛选 - 使用精确匹配
            if genres:
                genre_conditions = Q()
                for genre in genres:
                    genre_conditions |= Q(genres__contains=genre)
                queryset = queryset.filter(genre_conditions)
                print(f"应用类型筛选后的结果数: {queryset.count()}")

            # 分页
            total = queryset.count()
            offset = (page - 1) * page_size
            limit = offset + page_size
            games = queryset[offset:limit]

            # 打印调试信息
            print(f"最终查询到 {len(games)} 条结果")
            if len(games) > 0:
                print("示例游戏:", games[0].name, games[0].platform, games[0].genres)

            serializer = GameSerializer(games, many=True)
            return Response({
                'code': 200, 
                'data': serializer.data,
                'total': total,
                'page': page,
                'pageSize': page_size
            })

        except Exception as e:
            print("筛选过程中出现错误:", str(e))
            import traceback
            traceback.print_exc()  # 打印完整的错误堆栈
            return Response({
                'code': 500,
                'message': f'筛选失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)