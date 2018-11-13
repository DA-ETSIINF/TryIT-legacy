from django.contrib import admin

from editions.models import Company, Edition, Speaker, SessionFormat, Session, Track, Prize, PrizeObject, SponsorType, \
    CompanySponsorType


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


class CompanySponsorTypeInline(admin.TabularInline):
    model = CompanySponsorType
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'url_cv')
    inlines = (CompanySponsorTypeInline,)
    ordering = ('name',)
    search_fields = ('name',)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',
                    'have_bio', 'have_picture', 'have_contact_email',
                    'have_phone_number', 'have_personal_web',
                    'have_twitter', 'have_github', 'have_gitlab',
                    'have_linkedin', 'have_facebook', 'have_google')
    search_fields = ('name', 'company__name')

    def have_bio(self, obj):
        return obj.bio != ''

    have_bio.boolean = True

    def have_picture(self, obj):
        return obj.picture != ''

    have_picture.boolean = True
    have_picture.short_description = u"PICTURE"

    def have_contact_email(self, obj):
        return obj.contact_email != ''
        # return u'<img src="%s" />' % obj.admin_thumbnail.url

    # _get_thumbnail.allow_tags = True
    have_contact_email.boolean = True
    have_contact_email.short_description = u"EMAIL"

    def have_phone_number(self, obj):
        return obj.phone_number != ''

    have_phone_number.boolean = True
    have_phone_number.short_description = u"PHONE"

    def have_personal_web(self, obj):
        return obj.personal_web != ''

    have_personal_web.boolean = True
    have_personal_web.short_description = u"WEB"

    def have_twitter(self, obj):
        return obj.twitter_profile != ''

    have_twitter.boolean = True
    have_twitter.short_description = u"TWITTER"

    def have_facebook(self, obj):
        return obj.facebook_profile != ''

    have_facebook.boolean = True
    have_facebook.short_description = u"FACEBOOK"

    def have_linkedin(self, obj):
        return obj.linkedin_profile != ''

    have_linkedin.boolean = True
    have_linkedin.short_description = u"LINKEDIN"

    def have_github(self, obj):
        return obj.github_profile != ''

    have_github.boolean = True
    have_github.short_description = u"GITHUB"

    def have_gitlab(self, obj):
        return obj.gitlab_profile != ''

    have_gitlab.boolean = True
    have_gitlab.short_description = u"GITLAB"

    def have_google(self, obj):
        return obj.googleplus_profile != ''

    have_google.boolean = True
    have_google.short_description = u"GOOGLE+"


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
