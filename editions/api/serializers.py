from django.contrib.auth.models import User
from rest_framework import serializers

from editions.models import Edition, Company, Session, Speaker, Track, Organizer, CompanySponsorType
from sponsorship.models import Sponsor
from tickets.models import School


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class EditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edition
        fields = ('url', 'year', 'title', 'slogan', 'description', 'start_date', 'end_date')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'url', 'sponsor_type' )


class SpeakerSerializer(serializers.ModelSerializer):
    # company = CompanySerializer(many=True, read_only=True)
    company = serializers.SerializerMethodField('getCompanyName')

    class Meta:
        model = Speaker
        fields = (
            'name', 'bio', 'image', 'company', 'personal_web',
            'twitter_profile', 'facebook_profile', 'linkedin_profile',
            'googleplus_profile', 'github_profile', 'gitlab_profile'
        )

    def getCompanyName(self, speaker):
        companiesString = ""
        if speaker.company:
            companiesString += speaker.company.name
        return companiesString


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('name', 'description', 'room')


class SessionSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)
    company = serializers.SerializerMethodField('getCompany')
    track = TrackSerializer(many=True, read_only=True)
    rooms = serializers.SerializerMethodField('getRooms')
    logo = serializers.SerializerMethodField('getCompanyLogo')

    class Meta:
        model = Session
        fields = ('title', 'start_date', 'end_date', 'description', 'url', 'video', 'company',
                  'logo', 'speakers', 'track', 'rooms')

    def getCompany(self, session):
        companiesString = ""
        if session.companies.all():
            for sesi in session.companies.all():
                companiesString += sesi.name + ", "
        return companiesString[:-2]

    def getCompanyLogo(self, session):
        if session.companies.all():
            comp = session.companies.all()[0]
            if comp and comp.logo:
                return comp.logo.url
            else:
                return None

    def getRooms(self, session):
        str = ""
        if session.track.all():
            for t in session.track.all():
                str += t.room + ", "
        return str[:-2]


class YearSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'title', 'start_date')


class SchoolSerializer(serializers.ModelSerializer):
    degrees = serializers.SerializerMethodField('getDegrees')

    class Meta:
        model = School
        fields = ('code', 'name', 'degrees')

    def getDegrees(self, school):
        return [{'code': degree.code, 'name': degree.degree} for degree in school.degree_set.all()]


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'


class SponsorsSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField('getCompanies')

    def getCompanies(self, sponsors):
        return CompanySerializer(sponsors.company, read_only=True,  context=self.context).data

    sponsor_type = serializers.SerializerMethodField('getSponsorType')

    def getSponsorType(self, sponsors):
        return sponsors.sponsor_type.name

    class Meta:

        model = CompanySponsorType
        fields = '__all__'