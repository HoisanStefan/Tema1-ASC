"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__(**kwargs)
        self.carts = carts
        self.market = marketplace
        self.wait_time = retry_wait_time

    def run(self):
        """
        For every cart in this consumer's carts, we extract the actions types,
        the quantity needed and the product's name. Then we call the functions
        in order to create the cart with all of the required products.
        """

        for cart in self.carts:
            index = self.market.new_cart()
            count = 0
            for _ in cart:
                action = cart[count]["type"]
                product = cart[count]["product"]
                quantity = cart[count]["quantity"]
                i = 0
                while i < quantity:
                    if "add" in action:
                        ok = self.market.add_to_cart(index, product)
                        if not ok:
                            sleep(self.wait_time)
                        else:
                            i += 1
                    else:
                        if "remove" in action:
                            self.market.remove_from_cart(index, product)
                            i += 1
                count += 1
            self.market.place_order(index)
