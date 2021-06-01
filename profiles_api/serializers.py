from django.contrib.auth.models import Group
from rest_framework import serializers
from profiles_api.models import Users


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = ('id', 'email', 'first_name', 'password', 'last_name', 'phone_number', 'birth_day', 'gender', 'groups')
		extra_kwargs = {
			'password': {
				'write_only': True,
				'style': {'input_type': 'password'}
			}
		}

	def create(self, validated_data):
		"""Create User"""
		user = Users.objects.create_user(**validated_data)
		return user

	def update(self, instance, validated_data):
		if 'password' in validated_data:
			validated_data.pop('password')

		if 'email' in validated_data:
			validated_data.pop('email')

		if 'first_name' in validated_data:
			instance.set_first_name = validated_data.get('first_name')

		if 'last_name' in validated_data:
			instance.set_last_name = validated_data.get('last_name')

		if 'phone_number' in validated_data:
			instance.set_phone_number = validated_data.get('phone_number')

		if 'birth_day' in validated_data:
			instance.set_birth_day = validated_data.get('birth_day')

		if 'gender' in validated_data:
			instance.set_gender = validated_data.get('gender')

		if 'is_active' in validated_data:
			instance.set_status = validated_data.get('is_active')

		return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name')

	def create(self, validated_data):
		group, created = Group.objects.get_or_create(name=validated_data['name'])
		return group
