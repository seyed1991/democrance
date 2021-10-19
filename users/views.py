from rest_framework import permissions, generics
from users import serializers
from users.models import User


class CustomerList(generics.ListAPIView):
    """
    :returns list of customers to the admin user
    """
    # TODO: implement filter
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = [permissions.IsAdminUser]


class CustomerCreation(generics.CreateAPIView):
    """
    Creates customer and :returns customer object to admin user
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [permissions.IsAdminUser]
