from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

from .models import User, Event, Available
from .serializers import UserSerialiazer, EventSerializer, AvailableSerializer
from .times import calculateTime
# no import validate

# Create your views here.

class UserView(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        users = User.objects.all()
        if("user_id" in request.GET):
            users = users.filter(id=request.GET["user_id"])
        results = self.paginate_queryset(users, request, view=self)
        serializer = UserSerialiazer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerialiazer(data=request.data)
        if "username" in request.data:
            users = User.objects.filter(username=request.data["username"])
            if(users):
                return Response(status=status.HTTP_409_CONFLICT)

        if serializer.is_valid():
            if "pic" in request.FILES:
                serializer.save(pic=request.FILES["pic"])
            else:
                serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventView(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        events = Event.objects.all()
        results = self.paginate_queryset(events, request, view=self)
        serializer = EventSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        # if(not user.id and "username" not in request.data):
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        if(user.id):
            user = User.objects.get(id=user.id)

            serializer = EventSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                time = request.data["time"]
                posibble_time = request.data["possible_time"]
                # if not validate(time) or validate(posibble_time):
                #     print("bad time")
                #     return Response(status=status.HTTP_400_BAD_REQUEST)

                serializer.save(owner=user)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = EventSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                time = request.data["time"]
                posibble_time = request.data["possible_time"]
                # if not validate(time) or validate(posibble_time):
                #     print("bad time")
                #     return Response(status=status.HTTP_400_BAD_REQUEST)

                serializer.save(anonowner=request.data["username"])
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FirstEventView(APIView):
    def post(self, request, format=None):
        event = Event.objects.filter(id=request.data["id"])
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
class AvailableView(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        if("id" not in request.GET):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event = Event.objects.filter(id=request.data["id"])
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event = event[0]
        times = Available.objects.all(event=event)
        # results = self.paginate_queryset(times, request, view=self)
        serializer = AvailableSerializer(times, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        if("id" not in request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(not user.id and "username" not in request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(user.id):
            user = User.objects.get(id=user.id)
            
            event = Event.objects.filter(id=request.data["id"])
            if not event:
                return Response(status=status.HTTP_404_NOT_FOUND)
            event = event[0]

            serializer = AvailableSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                time = request.data["time"]
                # if not validate(time):
                #     print("bad time")
                #     return Response(status=status.HTTP_400_BAD_REQUEST)

                serializer.save(user=user, event=event)
                times = []
                avialables = Available.objects.filter(event=event)
                for a in avialables:
                    times.append(a.time)
                new_time = calculateTime(times)
                event.time = new_time
                event.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            event = Event.objects.filter(id=request.data["event_id"])
            if not event:
                return Response(status=status.HTTP_404_NOT_FOUND)
            event = event[0]
    
            serializer = AvailableSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                time = request.data["time"]
                # if not validate(time):
                #     print("bad time")
                #     return Response(status=status.HTTP_400_BAD_REQUEST)

                serializer.save(anonuser=request.data["username"], event=event)
                times = []
                avialables = Available.objects.filter(event=event)
                for a in avialables:
                    times.append(a.time)
                new_time = calculateTime(times)
                event.time = new_time
                event.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendeeViews(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        if ("id" not in request.GET):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event = Event.objects.filter(id=request.GET["id"])
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event = event[0]
        times = Available.objects.all(event=event)
        results = self.paginate_queryset(times, request, view=self)
        serializer = AvailableSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
