from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.utils.crypto import get_random_string
from tinymce import models as tinymce_models

now =  datetime.now()
time = now.strftime("%d %B %Y")
# Create your models here.
class Post(models.Model):
    postname = models.CharField(max_length=600)
    CATEGORY_CHOICES = [
        ('Programming', 'Programming'),
        ('Travel', 'Travel'),
        ('Education', 'Education'),
        ('Technology', 'Technology'),
        ('ArtificialIntelligence', 'ArtificialIntelligence'),
    ]
    category = models.CharField(max_length=600, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='images/posts',blank=True,null=True)
    content = tinymce_models.HTMLField()
    time = models.CharField(default=time,max_length=100, blank=True)
    likes = models.IntegerField(null=True,blank=True,default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    # New field to track the post status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return str( self.postname)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    time = models.CharField(default=time,max_length=100, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.user} Commented on - {self.post} , {self.time}"
    

class Contact(models.Model):
    name = models.CharField(max_length=600)
    email = models.EmailField(max_length=600)
    subject = models.CharField(max_length=1000)
    message = models.CharField(max_length=10000, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    

class PasswordResetToken(models.Model):
    """
    Model to manage password reset tokens with enhanced security features
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='password_reset_token'
    )
    token = models.CharField(
        max_length=64, 
        unique=True, 
        null=False, 
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Password Reset Token for {self.user.username}"
    
    def is_expired(self, hours=24):
        """
        Check if the token has expired
        
        Args:
            hours (int): Token expiration time in hours. Defaults to 24.
        
        Returns:
            bool: True if token is expired, False otherwise
        """
        expiration_time = self.created_at + timezone.timedelta(hours=hours)
        return timezone.now() > expiration_time
    
    def generate_token(self):
        """
        Generate a unique reset token
        
        Returns:
            str: Unique reset token
        """
        return get_random_string(length=64)
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure token is set
        """
        if not self.token:
            self.token = self.generate_token()
        
        super().save(*args, **kwargs)
    
    @classmethod
    def create_token_for_user(cls, user):
        """
        Create a new reset token for a user, 
        invalidating any existing tokens
        
        Args:
            user (User): Django User instance
        
        Returns:
            PasswordResetToken: Newly created token instance
        """
        # Delete any existing tokens for this user
        cls.objects.filter(user=user).delete()
        
        # Create and return a new token
        return cls.objects.create(user=user)