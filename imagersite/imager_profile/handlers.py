# coding=utf-8
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from imager_profile.models import ImagerProfile
from django.conf import settings
from django.dispatch import receiver
from logging import Logger

logger = Logger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_imager_profile(sender, **kwargs):
    if kwargs.get('created', False):
        try:
            new_profile = ImagerProfile(user=kwargs['instance'])
            new_profile.save()
        except (ValueError):
            msg = 'Unable to create ImagerProfile for {}'
            logger.error(msg.format(kwargs['instance']))


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_imager_profile(sender, **kwargs):
    try:
        kwargs['instance'].profile.delete()
    except (KeyError, AttributeError):
        msg = 'Unable to delete instance for {}'
        logger.warning(msg.format(kwargs['instance']))
