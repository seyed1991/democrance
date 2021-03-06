"""democrance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import users.views as users_views
import insurance.views as insurance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),  # basic django rest framework login/logout views
    path('api/v1/list_customers/', users_views.CustomerList.as_view()),
    path('api/v1/create_customer/', users_views.CustomerCreation.as_view()),
    path('api/v1/quote/', insurance_views.QuoteList.as_view()),
    path('api/v1/policies/', insurance_views.PolicyList.as_view()),
    path('api/v1/policies/<int:policy_id>/', insurance_views.PolicyDetail.as_view()),
    path('api/v1/policies/<int:policy_id>/history/', insurance_views.PolicyHistory.as_view()),
]
