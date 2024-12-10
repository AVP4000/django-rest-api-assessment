"""View module for handling requests about SongGenres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre

class SongGenreView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single songGenre 
        Returns:
            Response -- JSON serialized songGenre 
        """
        try:
            song_genre = SongGenre.objects.get(pk=pk)
            serializer = SongGenreSerializer(song_genre)
            return Response(serializer.data)
        except SongGenre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all SongGenres 

        Returns:
            Response -- JSON serialized list of SongGenres
        """
        song_genres = SongGenre.objects.all()

        serializer = SongGenreSerializer(song_genres, many=True)
        return Response(serializer.data)


class  SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = SongGenre
        fields = ('song', 'genre')

        