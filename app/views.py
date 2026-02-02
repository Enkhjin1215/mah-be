from rest_framework import viewsets
from .models import Lottery
from .serializers import LotterySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer



class LotteryNumberAllView(APIView):
    def get(self, request):
        last_7_days = timezone.now() - timedelta(days=7)

        numbers = list(
            Lottery.objects.filter(created_at__gte=last_7_days)
            .order_by("-created_at")
            .values_list("lottery_number", flat=True)
        )

        return Response(numbers)


class LotteryByPhoneView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({'error': 'phone_number parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        lotteries = Lottery.objects.filter(phone_number=phone_number)
        serializer = LotterySerializer(lotteries, many=True)
        return Response(serializer.data)