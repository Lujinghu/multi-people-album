from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Album, Photo
from .serializers import AlbumSerializer, PhotoSerializer
from . import permissions


class AlbumList(APIView):
    def get(self, request, format=None):
        user = request.user
        albums = user.album_set.all()
        albums_serializer = AlbumSerializer(albums, many=True)
        context = {'data1': albums_serializer.data} # because there is different albums so we need to specify them.
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        album_serializer = AlbumSerializer(data=request.data)
        if album_serializer.is_valid():
            album_serializer.save(creater=request.user)
            return Response(album_serializer.data, status=status.HTTP_201_CREATED)
        return Response(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetail(APIView):
    permission_classes = (permissions.IsAlbumSharerOrNoPermission, permissions.IsAlbumCreaterOrReadOnly)

    def get_object(self, album_id):
        return get_object_or_404(Album, id=album_id)

    def get(self, request, album_id):
        album = self.get_object(album_id)
        album_serializer = AlbumSerializer(album) #I still have question that how the serializer serialize the photos
        return Response(album_serializer.data)

    def put(self, request, album_id):
        album = self.get_object(album_id)
        album_serializer = AlbumSerializer(album, data=request.data)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(album_serializer.data)
        return Response(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album_id):
        album = self.get_object(album_id)
        album.delete() # I am such a pity, obviously it can be deleted by the instance ifself, we don't need a serializer.
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoList(APIView):
    permission_classes = (permissions.IsAlbumSharerOrNoPermission, )

    def get(self, request, album_id=None):
        if album_id is None:
            photos = request.user.photo_set.all()
            photo_serializer = PhotoSerializer(photos, many=True)
            return Response(photo_serializer.data, status=status.HTTP_200_OK)
        album = get_object_or_404(Album, id=album_id)
        self.check_object_permissions(request, album) # call this method to check the permission myself.
        photos = album.photo_set.all()
        photo_serializer = PhotoSerializer(photos, many=True)
        return Response(photo_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, album_id):
        album = get_object_or_404(Album, album_id)
        self.check_object_permissions(request, album)
        photo_serializer = PhotoSerializer(data=request.data)
        if photo_serializer.is_valid():
            photo_serializer.save(creater=request.user, album=album)
            return Response(photo_serializer.data, status=status.HTTP_201_CREATED)
        return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoDetail(APIView):
    permission_classes =(permissions.IsPhotoSharerOrNoPermission, permissions.IsPhotoCreaterOrReadOnly)

    def get(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
        self.check_object_permissions(request, photo)
        photo_serializer = PhotoSerializer(photo) #Before return to the client, must serialize and render
        return Response(photo_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
        self.check_object_permissions(request, photo)
        photo_serializer = PhotoSerializer(photo, data=request.data)
        if photo_serializer.is_valid():
            photo_serializer.save()
            return Response(photo_serializer.data)
        return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
        self.check_object_permissions(request, photo)
        photo.delete()
        return Response(status.HTTP_204_NO_CONTENT)