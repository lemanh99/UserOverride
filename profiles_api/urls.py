from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles_api.views import UserProfileViewSet, UserLoginApiView, ListGroupView, LogoutView, ListUserItemView

router = DefaultRouter()
router.register('users', UserProfileViewSet)
urlpatterns = [
    path('group/', ListGroupView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('users/<int:id>/', ListUserItemView.as_view()),
    path('', include(router.urls))
]
