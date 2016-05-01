# coding=utf-8
from django.db.models.signals import pre_save
from imager_images.models import Photo, PUBLIC
from django.dispatch import receiver
from datetime import datetime


@receiver(pre_save, sender=Photo)
def set_published_date(sender, instance=None, **kwargs):
    """Set the date_published field to the appropriate value based on its
    current value and the value of the PUBLISHED field"""
    if instance.published == PUBLIC:
        if not instance.date_published:
            instance.date_published = datetime.now()
    else:
        instance.date_published = None
