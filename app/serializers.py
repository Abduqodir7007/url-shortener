from rest_framework import serializers
from .models import User, Url
from django.contrib.auth import get_user_model
from .utils import generate_random_url


class UserRegisterSer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserLoginSer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]


class UrlSer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()  
    custom_url = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = Url
        fields = ["id", "original_url", "short_url", "click_count", "is_active","custom_url"]
        
    

    def validate_short_url(self, value):
        if Url.objects.filter(short_url=value).exists():
            raise serializers.ValidationError(
                "This custom short code is already taken."
            )
        return value

    def get_short_url(self, obj):
        return f"https://127.0.0.1:8000/{obj.short_url}"
    
    def create(self,validated_data):
        custom = validated_data.pop('custom_url', None)
        if custom:
            if Url.objects.filter(short_url=custom).exists():
                raise serializers.ValidationError("This custom short code is already taken.")
            validated_data['short_url'] = custom
        else:
            url = generate_random_url()
            while Url.objects.filter(short_url=url).exists():
                url = generate_random_url()
            validated_data['short_url'] = url
            
        return super().create(validated_data)
