"""
kombu.transport.ElasticMQ
===================

TODO:  Clean this up!
Amazon SQS transport module for Kombu. This package implements an AMQP-like
interface on top of Amazons SQS service, with the goal of being optimized for
high performance and reliability.

The default settings for this module are focused now on high performance in
task queue situations where tasks are small, idempotent and run very fast.

SQS Features supported by this transport:
  Long Polling:
    http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/
      sqs-long-polling.html

    Long polling is enabled by setting the `wait_time_seconds` transport
    option to a number > 1. Amazon supports up to 20 seconds. This is
    disabled for now, but will be enabled by default in the near future.

  Batch API Actions:
   http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/
     sqs-batch-api.html

    The default behavior of the SQS Channel.drain_events() method is to
    request up to the 'prefetch_count' messages on every request to SQS.
    These messages are stored locally in a deque object and passed back
    to the Transport until the deque is empty, before triggering a new
    API call to Amazon.

    This behavior dramatically speeds up the rate that you can pull tasks
    from SQS when you have short-running tasks (or a large number of workers).

    When a Celery worker has multiple queues to monitor, it will pull down
    up to 'prefetch_count' messages from queueA and work on them all before
    moving on to queueB. If queueB is empty, it will wait up until
    'polling_interval' expires before moving back and checking on queueA.
"""

from __future__ import absolute_import

from boto.sqs import SQSRegionInfo
from boto.sqs.connection import SQSConnection

from kombu.transport.SQS import Transport as SQSTransport
from kombu.transport.SQS import Channel as SQSChannel

from . import virtual

class Channel(SQSChannel):
    def _aws_connect_to(self, fun, regions):
        from boto.sqs import SQSRegionInfo
        conninfo = self.conninfo
        region_name = '%s:%s' % (self.conninfo.hostname, self.conninfo.port)
        region = SQSRegionInfo(connection=SQSConnection, name=region_name, endpoint=self.conninfo.hostname)
        return fun(is_secure=False,
                   region=region,
                   aws_access_key_id=conninfo.userid,
                   aws_secret_access_key=conninfo.password,
                   port=conninfo.port)

class Transport(SQSTransport):
    Channel = Channel
    driver_name = 'emq'
