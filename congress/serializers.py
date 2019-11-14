from rest_framework.serializers import ModelSerializer

from congress.models import Streaming


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

class OrganizerSerializer():
    pass


# Serializer to retrieve all organizers of an Edition
# It will use OrganizerSerializer
# Making two different serializers to improve readability and modularity


class EditionOrganizersSerializer():
    pass