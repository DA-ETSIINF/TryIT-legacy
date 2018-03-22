from django.contrib import admin

from editions.models import Company, Edition, Speaker, SessionFormat, Session, Track, Prize, PrizeObject, SponsorType


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
    list_display = ('session', 'have_winner', 'hide', 'company', 'prize_object', 'name')
    ordering = ('session__start_date',)

    def have_winner(self, obj):
        return obj.winner is not None

    have_winner.boolean = True


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sponsor_type', 'url', 'url_cv')
    actions = ('remove_sponsor_type',)

    def remove_sponsor_type(self, request, queryset):
        for obj in queryset:
            obj.sponsor_type = None
            obj.save()

    remove_sponsor_type.short_description = 'Remove sponsor type'


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'have_picture', 'have_twitter',
                    'have_github', 'have_gitlab', 'have_linkedin', 'have_google', 'have_facebook')
    search_fields = ('name', 'company__name')

    def have_picture(self, obj):
        return obj.picture != ''

    have_picture.boolean = True

    def have_twitter(self, obj):
        return obj.twitter_profile != ''

    have_twitter.boolean = True

    def have_facebook(self, obj):
        return obj.facebook_profile != ''

    have_facebook.boolean = True

    def have_linkedin(self, obj):
        return obj.linkedin_profile != ''

    have_linkedin.boolean = True

    def have_github(self, obj):
        return obj.github_profile != ''

    have_github.boolean = True

    def have_gitlab(self, obj):
        return obj.gitlab_profile != ''

    have_gitlab.boolean = True

    def have_google(self, obj):
        return obj.googleplus_profile != ''

    have_google.boolean = True


admin.site.register(Company, CompanyAdmin)
admin.site.register(Edition)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(SessionFormat)
admin.site.register(Session, SessionAdmin)
admin.site.register(Track)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(PrizeObject)
admin.site.register(SponsorType)
