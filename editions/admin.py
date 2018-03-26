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


class EditionAdmin(admin.ModelAdmin):
    list_display = ('year',
                    'title', 'slogan', 'description',
                    'start_date', 'end_date',
                    'have_google_calendar_url')

    def have_google_calendar_url(self, obj):
        return obj.google_calendar_url != ""
    have_google_calendar_url.boolean = True


class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'description')


class PrizeAdmin(admin.ModelAdmin):
    list_filter = ('session__edition__year',)
    list_display = ('session', 'have_winner', 'hide', 'company', 'prize_object', 'name')
    ordering = ('session__start_date',)
    raw_id_fields = ('winner',)

    def have_winner(self, obj):
        return obj.winner is not None

    have_winner.boolean = True


class PrizeObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'have_image', 'description')

    def have_image(self, obj):
        return obj.image != ""
    have_image.boolean = True


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


class SponsorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(SessionFormat)
admin.site.register(Session, SessionAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(PrizeObject, PrizeObjectAdmin)
admin.site.register(SponsorType, SponsorTypeAdmin)
