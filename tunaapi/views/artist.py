from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
from tunaapi.models import Artist, Song

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artist"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
        depth=1
        
class SingleArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'songs', 'song_count')
        depth = 1
        
class ArtistView(ViewSet):
    """Tuna artists view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist"""
        try:
            artist = Artist.objects.annotate(song_count=Count('songs')).get(pk=pk)
            serializer = SingleArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all artists"""
        artists = Artist.objects.annotate(song_count=Count('songs')).all()

        serializer = SingleArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized artist instance
        """

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an artist
        
        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()
        serializer = ArtistSerializer(artist)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """Handle DELETE requests for an artist"""
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

