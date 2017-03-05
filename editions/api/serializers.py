from django.contrib.auth.models import User
from rest_framework import serializers

import json

from editions.models import Edition, Company, Session, Speaker, Track


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
        fields = ('name', 'logo', 'url')


class SpeakerSerializer(serializers.ModelSerializer):
    # company = CompanySerializer(many=True, read_only=True)
    company = serializers.SerializerMethodField('getCompanyName')

    class Meta:
        model = Speaker
        fields = (
            'name', 'bio', 'picture', 'company', 'personal_web',
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
    #companyOBJ = CompanySerializer(many=True, read_only=True)
    track = TrackSerializer(many=True, read_only=True)
    rooms = serializers.SerializerMethodField('getRooms')
    #logo = serializers.SerializerMethodField('getCompanyLogo')

    class Meta:
        model = Session
        fields = ('title', 'start_date', 'end_date', 'description', 'url', 'video', 'company',
                  #'companyOBJ',
                  #'logo',
                  'speakers', 'track', 'rooms')

    def getCompany(self, session):
        companiesString = ""
        if session.companies.all():
            for sesi in session.companies.all():
                companiesString += sesi.name + ", "
        return companiesString[:-2]

    # def getCompanyLogo(self, session):
    #     if session.companies.all():
    #         for comp in session.companies.all():
    #             return comp.logo

    def getRooms(self, session):
        str = ""
        if session.track.all():
            for t in session.track.all():
                str += t.room + ", "
        return str[:-2]


class YearSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('code', 'title', 'start_date')
