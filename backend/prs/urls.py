from rest_framework.routers import DefaultRouter
from .views import PullRequestViewSet
r=DefaultRouter(); r.register('prs',PullRequestViewSet,basename='prs')
urlpatterns=r.urls
