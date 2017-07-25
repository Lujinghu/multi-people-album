from rest_framework import permissions


class IsPhotoSharerOrNoPermission(permissions.BasePermission):
    '''
    Only the album's sharers can visit the photo
    '''
    def has_object_permission(self, request, view, obj):
        return request.user in obj.album.sharers.all()


class IsAlbumSharerOrNoPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.sharers.all()


class IsAlbumCreaterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.creater


class IsPhotoCreaterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.creater

