from rest_framework import serializers
from .models import User, Event, Available

class UserSerialiazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "pic"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class EventSerializer(serializers.HyperlinkedModelSerializer):
    # owner = UserSerialiazer(required=False)
    class Meta:
        model = Event
        fields = ["name", "id", "time", "possible_time"]


class AvailableSerializer(serializers.HyperlinkedModelSerializer):
    event = EventSerializer(required=False)
    user = UserSerialiazer(required=False)
    class Meta:
        model = Available
        fields = ["user", "name", "event", "time"]
        extra_kwargs = {
            "user": {"read_only": True},
            "name": {"read_only": True},
            "event": {"read_only": True},
        }

