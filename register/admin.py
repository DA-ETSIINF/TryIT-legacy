from django.contrib import admin

from register.models import RegisterCompany



class RegisterCompanyAdmin(admin.ModelAdmin):
    list_display = ('contact_name',
                    'company',
                    'email', 'phone',
                    'is_sponsor', 'sponsor_type', 'sponsor_date',
                    'type', 'topic', 'description',
                    'have_document'
                    )

    def is_sponsor(self, obj):
        return obj.sponsor
    is_sponsor.boolean = True

    def have_document(self, obj):
        return obj.document != ""
    have_document.boolean = True

    list_filter = ('sponsor', 'sponsor_type', 'sponsor_date', 'type')
    search_fields = ('contact_name', 'company', 'email', 'phone', 'type', 'topic', 'description')



admin.site.register(RegisterCompany, RegisterCompanyAdmin)
