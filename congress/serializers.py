from rest_framework.serializers import ModelSerializer

from congress.models import Streaming
from editions.models import Session


class StreamingSerializer(ModelSerializer):


    class Meta:
        model = Streaming
        fields = '__all__'


class EditionSerializer(ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'


