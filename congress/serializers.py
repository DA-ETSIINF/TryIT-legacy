from rest_framework.serializers import ModelSerializer

from congress.models import Streaming

class StreamingSerializer(ModelSerializer):


    class Meta:
        model = Streaming
        fields = '__all__'


