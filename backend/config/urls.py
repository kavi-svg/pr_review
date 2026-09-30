from django.contrib import admin
from django.urls import include, path
urlpatterns=[path('admin/',admin.site.urls),path('api/',include('prs.urls')),path('api/evaluation/',include('evaluation.urls'))]
