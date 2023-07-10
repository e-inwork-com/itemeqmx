"""
TODO
"""
import uuid
from django.db import models


class ItemSubscribe(models.Model):
    """
    Item Subscribe Model

    - A scanner sends a message to EQMX server in a format
      {SN: XXXXABC, MSG: (EAN21)}

    - When create a record of the Item Subscribe Model will be automatically
      send a task to create, update or remove the Item Model

    TODO
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    topic = models.CharField(max_length=55, unique=True)
    payload = models.JSONField()


class Item(models.Model):
    """
    Item Model

    - A scanner sends a message to EQMX server in a format
      {SN: XXXXABC, MSG: (EAN21)}

    - SN represents the unique ID for location.

    - EAN has to be split into three strings of fixed length.
      <Serial>, <LOT>, <DATE>

    - App searches for Item with <Serial>.
      If such item exists, then check the SN (location id) ,
      if SN the same, then change status to “Removed” and append
      the date of update, else if SN is not the same, update SN and
      append date of update, else create instance of ITEM with
      SN, SERIAL and DATE and date of update

    TODO
    """
    CREATED = 'created'
    UPDATED = 'updated'
    REMOVED = 'removed'
    STATUS = (
        (CREATED, 'Created'),
        (UPDATED, 'Updated'),
        (REMOVED, 'Removed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sn = models.CharField(max_length=6)
    serial = models.CharField(max_length=10, unique=True)
    lot = models.CharField(max_length=2)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default=CREATED)

    class Meta:
        unique_together = ('sn', 'serial')
