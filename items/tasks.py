"""
TODO
"""
from django.conf import settings

import paho.mqtt.client as mqtt

from itemmqmx.celery import app
from items.models import ItemSubscribe, Item


@app.task
def item_subscriber_create(topic, payload):
    """
    Create Item Subscriber
    """
    ItemSubscribe.objects.create(
        topic=topic,
        payload=payload
    )


@app.task
def item_subscriber_post_save(_id):
    """
    Created, update, or remove the Item
    - App searches for Item with <Serial>.
      If such item exists, then check the SN (location id) ,
      if SN the same, then change status to “Removed” and append
      the date of update, else if SN is not the same, update SN and
      append date of update, else create instance of ITEM with
      SN, SERIAL and DATE and date of update

    TODO
    """
    item_subscriber = ItemSubscribe.objects.get(id=_id)

    # Create, update or remove the Item
    # TODO: ...
    Item.objects.create(
        sn=item_subscriber.payload.get('SN'),
        # TODO: ...
    )

    # TODO: ...


def on_connect(client, userdata, flags, rc):
    """
    On Connected

    TODO:
    """
    print(f'Connected with result code {rc}')
    client.subscribe(settings.MQTT_CLIENT['TOPIC'])


def on_message(client, userdata, msg):
    """
    On getting a message

    TODO:
    """
    item_subscriber_create.delay(
        topic=msg.topic,
        payload=msg.payload
    )


@app.task
def run_mqtt_client():
    """
    Run MQTT Client

    TODO:
    """
    # Initial client
    client = mqtt.Client()

    # Specify callback function
    client.on_connect = on_connect
    client.on_message = on_message

    # Establish a connection
    client.connect(settings.MQTT_CLIENT['HOST'], settings.MQTT_CLIENT['PORT'])

    # Run forever
    client.loop_forever()
