from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models


class UserProfileManager(BaseUserManager):
	def create_user(
		self, email, password=None, first_name=None,
		last_name=None, phone_number=None, birth_day=None, gender=None, groups=None):
		try:
			group = Group.objects.get(name=groups)
		except Group.DoesNotExist:
			count = Group.objects.count()
			if count == 0:
				group, created = Group.objects.get_or_create(name='admin')
				group.save()
			else:
				raise ValueError("Required Create Group Before")

		if not email:
			raise ValueError("Required Email")
		email = self.normalize_email(email)
		user = self.model(
			email=email, first_name=first_name, last_name=last_name,
			phone_number=phone_number, birth_day=birth_day, gender=gender, groups_id=group.id)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email=email, password=password, groups='admin')
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user


class Users(AbstractBaseUser, PermissionsMixin):
	"""  Models Base """
	MALE = 'ML'
	FEMALE = 'FML'
	ORTHER = 'OTH'
	genders = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
		(ORTHER, 'Other'),
	)
	groups = models.ForeignKey(Group, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(unique=True, max_length=100, null=False)
	password = models.CharField(max_length=100, null=False)
	phone_number = models.CharField(max_length=15, null=True, blank=True)
	birth_day = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=100, choices=genders, default=MALE, null=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserProfileManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['password']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def get_full_name(self):
		return self.first_name + self.last_name

	def __str__(self):
		return self.email
