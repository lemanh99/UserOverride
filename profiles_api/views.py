from django.contrib.auth.models import Group
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from profiles_api.models import Users
from profiles_api.permissions import IsAdmin
from profiles_api.serializers import UserSerializer, GroupSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = Users.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAdmin,)
	filter_backends = (filters.SearchFilter,)
	search_fields = ('email',)


class UserLoginApiView(ObtainAuthToken):
	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

	def post(self, request, *args, **kwargs):
		response = super(UserLoginApiView, self).post(request, *args, **kwargs)
		token = Token.objects.get(key=response.data['token'])
		email = request.data['username']
		user = Users.objects.get(email=email)
		serializers = UserSerializer(user)
		return Response(
			{'token': token.key, 'user': serializers.data})


class LogoutView(APIView):
	authentication_classes = (TokenAuthentication,)

	def get(self, request, format=None):
		request.user.auth_token.delete()
		return Response(dict(message="Logout success"), status=status.HTTP_200_OK)


class ListUserItemView(APIView):
	"""
	Get, update information, delete item user
	"""

	def get(self, request, id, format=None):
		try:
			user = Users.objects.get(id=id)
			if user:
				serializer = UserSerializer(user)
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(status=status.HTTP_404_NOT_FOUND)

		except Users.DoesNotExist:
			return Response(dict(message="Not found"),
			                status=status.HTTP_404_NOT_FOUND)

	def put(self, request, id, format=None):
		try:
			user = Users.objects.get(id=id)
			serializer = UserSerializer(instance=user)
			serializer.update(instance=user,
			                  validated_data=request.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except Users.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, id, format=None):
		if id:
			try:
				user = Users.objects.get(id=id)
				user.delete()
				return Response(dict(message="Delete message success"),
				                status=status.HTTP_200_OK)

			except Users.DoesNotExist:
				return Response(dict(message="Not found"),
				                status=status.HTTP_404_NOT_FOUND)
		return Response(status=status.HTTP_404_NOT_FOUND)


class ListGroupView(APIView):
	"""
	GROUPS = ['admin', 'manager', 'user']
	"""
	serializer_class = GroupSerializer
	permission_classes = (IsAdmin,)
	authentication_classes = (TokenAuthentication,)

	def get(self, request, format=None):
		groups = Group.objects.all()
		serializer = GroupSerializer(groups, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = GroupSerializer(data=dict(name=request.data['name']))
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
