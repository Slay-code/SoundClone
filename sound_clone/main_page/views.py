from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from .models import Track
from .serializers import TrackSerializer, AddMySongsSerializer, MySongsSerializer


class TrackList(ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    
    
class TrackDetail(RetrieveDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    
    
class AddMySongs(CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = AddMySongsSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Получаем ID трека из URL (pk)
        track_id = self.kwargs['pk']  # Используем pk
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            raise ValidationError("Трек с таким ID не найден.")

        # Проверка, что трек не добавлен в "Мои песни"
        if track.user.filter(id=self.request.user.id).exists():
            raise ValidationError("Этот трек уже в ваших 'Моих песнях'.")

        # Добавляем трек в "Мои песни"
        track.user.add(self.request.user)
        return track

    def create(self, request, *args, **kwargs):
        # Используем perform_create для добавления трека
        track = self.perform_create(self.get_serializer())
        return Response({"message": f"Трек '{track.name}' успешно добавлен в 'Мои песни'."}, status=status.HTTP_201_CREATED)
        
        
class MySongs(ListAPIView):
    serializer_class = MySongsSerializer
    
    def get_queryset(self):
        return Track.objects.filter(user=self.request.user)

