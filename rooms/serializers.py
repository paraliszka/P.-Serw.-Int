from rest_framework import serializers
from .models import Rooms, Topic, Message, RoomRating


class RoomsSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    host = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Rooms
        fields = "__all__"

    def get_rating(self, obj):
        return obj.get_rating()

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)
    room = serializers.ReadOnlyField(source='room.name')
    class Meta:
        model = Message
        fields = "__all__"

class RoomRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    room = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RoomRating
        fields = "__all__"