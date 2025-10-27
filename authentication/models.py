from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with role-based access"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True, help_text='Avatar image URL')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def is_instructor(self):
        return self.role == 'instructor'

    def is_student(self):
        return self.role == 'student'

    def is_staff_member(self):
        return self.role == 'staff'

    def is_admin(self):
        return self.role == 'admin'


class InstructorFollow(models.Model):
    """Track student following instructors"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_instructors')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'instructor']
        verbose_name = 'Instructor Follow'
        verbose_name_plural = 'Instructor Follows'
        ordering = ['-followed_at']

    def __str__(self):
        return f"{self.student.username} follows {self.instructor.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'auth_profile'):
        instance.auth_profile.save()
