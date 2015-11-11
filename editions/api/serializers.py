from django.contrib.auth.models import User
from editions.models import Edition, Company, Track
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class EditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edition
        fields = ('url', 'year', 'title', 'slogan', 'description', 'start_date', 'end_date')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = (
            'url',
            'name',
            'description',
            'contact_person',
            'contact_email',
            'phone_number',
        )

class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('url', 'edition', 'code', 'title', 'description', 'format', 'start_date', 'end_date', 'companies', 'speakers')
