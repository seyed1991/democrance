import datetime
from django.db.models import Value
from django.db.models.functions import Concat
from rest_framework import permissions, generics

from users import serializers, models


class CustomerList(generics.ListAPIView):
    """
    :returns list of customers to the admin user
    """
    serializer_class = serializers.UserListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = models.User.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(full_name__icontains=name)
        date_of_birth = self.request.query_params.get('dob')
        if date_of_birth:
            queryset = queryset.filter(date_of_birth=datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date())
        return queryset


class CustomerCreation(generics.CreateAPIView):
    """
    Creates customer and :returns customer object to admin user
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [permissions.IsAdminUser]
