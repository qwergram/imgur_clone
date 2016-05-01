# coding=utf-8
from django.db.models.signals import pre_save
from imager_images.models import Photo, PUBLIC
from django.dispatch import receiver
from datetime import datetime


@receiver(pre_save, sender=Photo)
def set_published_date(sender, **kwargs):
    """Set the date_published field to the appropriate value based on its
    current value and the value of the PUBLISHED field"""
    if sender.published == PUBLIC:
        if not sender.date_published:
            sender.date_published = datetime.utcnow()
    else:
        sender.date_published = None
