import pandas as pd
from django.contrib import admin
from django.http import HttpResponse
from .models import Lottery


def export_lottery_to_excel(modeladmin, request, queryset):
    data = []
    for obj in queryset:
        naive_created_at = obj.created_at.astimezone(None).replace(tzinfo=None)
        data.append({
            'Phone number': obj.phone_number,
            'Lottery number': obj.lottery_number,
            'Aimag': obj.aimag,
            'Sum': obj.sum,
            'Horoo': obj.horoo,
            'Status': obj.status,
            'Created at': naive_created_at,
            'Ebarimt Picture': obj.ebarimt_picture.url if obj.ebarimt_picture else '',
        })
    
    df = pd.DataFrame(data)
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=lotteries.xlsx'
    
    df.to_excel(response, index=False)
    return response

export_lottery_to_excel.short_description = "Export selected lotteries to Excel"


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'lottery_number', 'aimag', 'sum', 'horoo', 'status', 'created_at')
    search_fields = ('phone_number', 'lottery_number', 'aimag', 'sum', 'horoo', 'status')
    list_filter = ('aimag', 'sum', 'horoo', 'status')
    actions = [export_lottery_to_excel]
