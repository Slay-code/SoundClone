from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class AddMySongsSerializer(serializers.Serializer):
    def validate_track_id(self, value):
        """
        Проверяем, существует ли трек с таким ID.
        """
        try:
            Track.objects.get(id=value)
        except Track.DoesNotExist:
            raise serializers.ValidationError("Трек с таким ID не найден.")
        return value

    def create(self, validated_data):
        """
        Добавляем трек в 'Мои песни' текущего пользователя.
        """
        track_id = validated_data['track_id']
        user = self.context['request'].user  # Получаем текущего пользователя
        track = Track.objects.get(id=track_id)

        # Проверяем, что трек не добавлен в "Мои песни" текущего пользователя
        if track.users.filter(id=user.id).exists():
            raise serializers.ValidationError("Этот трек уже в ваших 'Моих песнях'.")

        # Добавляем трек в "Мои песни"
        track.users.add(user)
        return track  # Возвращаем добавленный трек (для дальнейшего использования)


class MySongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['name', 'image', 'song', 'author', 'album']