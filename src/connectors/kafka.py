"""
The Kafka module contains classes and helpers to abstract out Kafka
operations and expose a uniform interface.

The module uses the confluent kafka library for Kafka operations,
which is based on librdkafka. In essense, all of the Kafka APIs
are executed in C context, and it allows us to offload a lot
of concurrency primitives (ex: producer queue) to librdkafka.
"""

from ..event import Event
from ..connect import SourceConnector, SinkConnector

from confluent_kafka import Producer, Consumer, KafkaException


class KafkaSourceConnector(SourceConnector):
    """
    Implements the Kafka source connector.

    Primarily, this is simple librdkafka based consumer
    that polls for messages until there is a keyboard interrupt
    or an exception and return an iterator for the consumed events
    """
    def __init__(self, config, topics, poll_timeout=1):
        self.consumer = Consumer(config)
        self.topics = topics
        self.poll_timeout = poll_timeout
        self.consumer.subscribe(self.topics)

    def events(self):
        """
        The events method implements the source connection
        events contract.

        It consumes the subscribed topics from the Kafka cluster.
        Returns an iterator that yield a consumed cdc event
        one at a time.
        """
        try:
            while True:
                message = self.consumer.poll(self.poll_timeout)
                if message is None:
                    print("poll timed out, continuing")
                    continue

                if message.error():
                    raise KafkaException(message.error())

                event = message.value().decode("utf-8")
                yield Event(event)

        except KeyboardInterrupt:
            pass

        finally:
            self.consumer.close()


class KafkaSinkConnector(SinkConnector):
    """
    Implements the Kafka sink connector.

    The connector is a producer wrapper on top of librdkafka,
    that produces events from the source stream to a
    kafka topic.

    Notes:
    1. Since this is a librdkafka based producer, there are no concurrency
    primitives implemented here. All of the queueing is handled by the
    underlying library. Essentially, the message gets queued in the
    internal librdkafka producer queues for async publish, and a callback
    is invoked for each produce result.

    2. In case of errors, there are a couple of approaches that could be
    taken (ex: ignore, fail fast, dlq topic etc). Currently, this implements
    the log and ignore model, but the connector could be extended to support
    others.
    """
    def __init__(self, config, topic):
        self.topic = topic
        self.producer = Producer(config)

    def __kcallback(self):
        """
        Return the produce callback function invoked by
        the kafka library (librdkafka). Currently, it implements a
        log and continue model.
        """
        def cb(err, msg):
            if err is not None:
                print("Message delivery failed: {}".format(msg))
            else:
                print(
                    "Message delivered to {}: {}".format(
                        msg.topic(), msg.partition()
                    )
                )

        return cb

    def publish(self, stream):
        """
        Implements the publish contract for the Kafka sink connector.
        It consumes the source stream, and publishes the events to Kafka.

        The cdc object key serves as the message key, and entire json is
        considered the value.
        """
        for event in stream:
            self.producer.produce(
                self.topic, key=event.key, value=event.raw,
                on_delivery=self.__kcallback()
            )

        self.producer.flush()
