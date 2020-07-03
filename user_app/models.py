from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from hero_app.models import Hero


class HeroApp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='heroapp')
    selected_hero = models.OneToOneField(Hero, on_delete=models.CASCADE, null=True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            HeroApp.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.heroapp.save()


# Create your models here.
