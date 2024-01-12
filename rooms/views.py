import django_filters.rest_framework
from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status, filters
from django.http import Http404
from .models import Rooms, Topic, Message, RoomRating
from .serializers import RoomsSerializer, TopicSerializer, MessageSerializer, RoomRatingSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS, IsAuthenticated, \
    IsAuthenticatedOrReadOnly


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(obj.host == request.user or request.user.is_staff)



class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

class RoomRatingCreate(generics.CreateAPIView):
    name = "room-rating-create"

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = RoomRating.objects.all()
    serializer_class = RoomRatingSerializer


    def perform_create(self, serializer):
        user = self.request.user
        room = Rooms.objects.get(pk=self.kwargs.get('pk'))
        rating = self.request.data.get('rating')
        existing_rating = RoomRating.objects.filter(user=user, room=room).first()
        if existing_rating:
            existing_rating.delete()
        else:
            serializer.save(user=user, room=room, rating=rating)

class RoomList(generics.ListAPIView):
    name = "room-list"
    queryset = Rooms.objects.all().annotate(rating=Sum('roomrating__rating')).order_by('-rating')
    serializer_class = RoomsSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'topic__name']

class RoomCreate(generics.CreateAPIView):
    name = "room-create"
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    name = "room-detail"
    serializer_class = RoomsSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrAdminOrReadOnly,)


    queryset = Rooms.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


class TopicsList(generics.ListCreateAPIView):
    name = "topic-list"

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    name = "topic-detail"

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


class MessagesList(generics.ListAPIView):
    name = "message-list"
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MessageCreate(generics.ListCreateAPIView):
    name = "message-create"
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        room_id = self.kwargs.get('pk')
        return Message.objects.filter(room=room_id)

    def perform_create(self, serializer):
        room_id = self.kwargs.get('pk')
        room_instance = Rooms.objects.get(pk=room_id)
        serializer.save(user=self.request.user, room=room_instance)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    name = "message-list"

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

class UserRatedRoomsList(generics.ListAPIView):
    name = "user-rated-rooms-list"
    serializer_class = RoomsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        rated_room_ids = RoomRating.objects.filter(user=user, rating__gt=0).values_list('room', flat=True)
        return Rooms.objects.filter(id__in=rated_room_ids)
