from rest_framework import serializers
from .models import Lottery, LotteryCampaign

class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = '__all__'

class LotteryCampaignSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.SerializerMethodField()

    class Meta:
        model = LotteryCampaign
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'is_ongoing', 'created_at', 'updated_at']

    def get_is_ongoing(self, obj):
        return obj.is_ongoing()
