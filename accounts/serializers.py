from rest_framework.serializers import ModelSerializer
from .models import KakaoUser, Post

class KaKaoUserSerializer(ModelSerializer):
    class Meta:
        model = KakaoUser
        fields = '__all__'
    
    
