"""core URL Configuration

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

from django.conf.urls import handler400
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)

from core.views import custom404,CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quiz_api.urls', namespace="quiz_api")),
    path("api/users/",include('users.urls'),name="users"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls'),name="rest_framwork"),
    path('__debug__/', include(debug_toolbar.urls)),
   
]
handler404=custom404
handler400=custom404
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
