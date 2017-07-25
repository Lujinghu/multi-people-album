from rest_framework import serializers

from .models import Album, Photo


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    photos = serializers.HyperlinkedRelatedField(many=True, view_name='photo-detail', read_only=True)

    class Meta:
        model = Album
        fields = ('url', 'id', 'name', 'photo_set')


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo

