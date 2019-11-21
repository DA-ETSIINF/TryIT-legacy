from rest_framework.serializers import ModelSerializer, SerializerMethodField

from congress.models import Streaming, Organizers

from editions.models import Edition

class StreamingSerializer(ModelSerializer):


    class Meta:
        model = Streaming
        fields = '__all__'


'''
    Serializer which receives an Organizer and gets all its data
    as:
    [
        {
        "name": "Organizername",
        "linkedin": "....",
        ....-
        }
    ]
'''

class OrganizerSerializer(ModelSerializer):

    class Meta:
        model = Organizers
        fields = '__all__'



# Serializer to retrieve all organizers of an Edition
# It will use OrganizerSerializer
# Making two different serializers to improve readability and modularity


class EditionOrganizersSerializer(ModelSerializer):

    organizers = SerializerMethodField()

    def get_organizers(self, edition_obj):
        return OrganizerSerializer(Organizers.objects.all().filter(edition=edition_obj), many=True).data

    class Meta:
        model = Edition
        fields = ("organizers", "year")