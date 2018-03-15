from django.contrib import admin

from editions.models import Company, Edition, Speaker, SessionFormat, Session, Track, Prize, PrizeObject


class SessionAdmin(admin.ModelAdmin):
    ordering = ('-start_date',)
    list_display = ('title', 'edition', 'start_date_format', 'end_date_format')
    list_filter = ('edition__year',)
    filter_horizontal = ('speakers', 'companies')

    def start_date_format(self, obj):
        if obj.start_date is None:
            return obj.start_date
        return obj.start_date.strftime('%e/%m - %H:%M')

    def end_date_format(self, obj):
        if obj.end_date is None:
            return obj.end_date
        return obj.end_date.strftime('%e/%m - %H:%M')

    start_date_format.admin_order_field = 'start_date'
    start_date_format.short_description = 'start date'
    end_date_format.admin_order_field = 'end_date'
    end_date_format.short_description = 'end date'


class PrizeAdmin(admin.ModelAdmin):
    list_filter = ('session__edition__year',)
    list_display = ('session', 'prize_object', 'name')


admin.site.register(Company)
admin.site.register(Edition)
admin.site.register(Speaker)
admin.site.register(SessionFormat)
admin.site.register(Session, SessionAdmin)
admin.site.register(Track)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(PrizeObject)
