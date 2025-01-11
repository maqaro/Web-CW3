from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    
    Hobbies = models.ManyToManyField(
        'Hobby', 
        related_name='users',
        null=True,
        blank=True
    )

    Profile = models.OneToOneField(
        'Profile',
        related_name='user_profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customeruser_set', 
        blank=True, 
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customeruser_set', 
        blank=True,
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username
    
class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1024, default='A cool hobby')

    class Meta:
        verbose_name_plural = 'Hobbies'

    def __str__(self):
        return self.name
    
class Friends(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='friendships', 
        null=True)
    
    friend = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='friends_with',
        null=True)

    friendship_status = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    status = models.CharField(max_length=8, choices=friendship_status, default='pending')
    
    class Meta:
        verbose_name_plural = 'Friends'

    def __str__(self):
        return f"{self.user} -> {self.friend} ({self.status})"

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        null=True)
    
    bio = models.CharField(max_length=1024, default='Write something about yourself')

    def __str__(self):
        return f"{self.bio} ({self.check_user})"
    
    @property
    def has_user(self):
        return hasattr(self, 'user') and self.user is not None
    
    @property
    def check_user(self):
        return str(self.user) if self.has_user else 'No user'

# this class is unneeded as we already have the abstract user model
# class UserAccount(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     username = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=128)  
#     date_created = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['username']
        
#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.username})"

# idk what this is for, it was here before so I'm leaving it here
# class PageView(models.Model):
#     count = models.IntegerField(default=0)

#     def __str__(self):
#         return f"Page view count: {self.count}"
