from users.models import User
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_of_birth']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_of_birth']
        read_only_fields = ['id', 'username']

    def to_internal_value(self, data):
        if not data.get('date_of_birth'):
            # manage `date_of_birth` field in request data
            data['date_of_birth'] = data['dob']

        return super(UserCreateSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        user = User(username=User.generate_username(validated_data), **validated_data)
        user.set_password(User.generate_password(validated_data))
        user.save()
        return user
