"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__(**kwargs)
        self.products = products
        self.market = marketplace
        self.wait_time = republish_wait_time

    def run(self):
        """
        Getting the producer id after registering him and then publishing his products
        list in an infinite loop
        """

        producer_id = self.market.register_producer()
        while True:
            for (product, quantity, wait_product) in self.products:
                for _ in range(quantity):
                    value = self.market.publish(producer_id, product)
                    if value:
                        sleep(wait_product)
                    else:
                        sleep(self.wait_time)
