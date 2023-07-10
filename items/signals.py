"""
TODO
"""
from django.db.models import signals
from django.dispatch import receiver

import items.tasks
from items.models import ItemSubscribe


@receiver(signals.post_save, sender=ItemSubscribe)
def item_subscriber_post_save(sender, instance, **kwargs):
    """
    Update Scan record and all related scan images
    """
    items.tasks.item_subscriber_post_save.delay(_id=instance.id)
