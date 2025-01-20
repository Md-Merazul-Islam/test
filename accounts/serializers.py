from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangeUserRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_role = serializers.ChoiceField(choices=['trainer', 'admin'])


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"error": "Passwords do not match."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['role'] = 'trainee'
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        # user.role = 'trainee'
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'phone_number', 'address']
        
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'address', 'is_paid']

    def update(self, instance, validated_data):
        # Allow only admins to change roles
        role = validated_data.get('role', instance.role)
        if role not in ['trainer', 'admin']:
            raise serializers.ValidationError("Invalid role.")
        
        return super().update(instance, validated_data)
