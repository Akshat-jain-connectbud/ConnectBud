from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserRoles(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    desc = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(
            default=timezone.now)

class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.TextField(null=True)
    password1 = models.TextField(null=True)
    password2 = models.TextField(null=True)
    facebook_id = models.TextField(null=True)


class UserWithroles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userroles = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)

