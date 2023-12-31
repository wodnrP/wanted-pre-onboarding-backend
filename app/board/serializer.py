from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('id', 'user', 'title', 'contents', 'create_time', 'update_time')
