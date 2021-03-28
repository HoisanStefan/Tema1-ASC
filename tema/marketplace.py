"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, currentThread


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size = queue_size_per_producer
        self.queues = []
        self.products = []
        self.no_of_carts = 0
        self.no_of_producers = 0
        self.producers = {}
        self.carts = {}
        self.lock_add_remove = Lock()
        self.lock_register = Lock()
        self.lock_place_order = Lock()
        self.lock_new_cart = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.lock_register:
            self.no_of_producers += 1
            self.queues.append(0)
        return self.no_of_producers - 1

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.queues[int(producer_id)] >= self.queue_size:
            return False
        else:
            self.products.append(product)
            self.queues[int(producer_id)] += 1
            self.producers[product] = int(producer_id)
            return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_new_cart:
            self.carts[self.no_of_carts] = []
            self.no_of_carts += 1
        return self.no_of_carts - 1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.lock_add_remove:
            if product not in self.products:
                return False
            else:
                self.products.remove(product)
                self.queues[self.producers[product]] -= 1
                self.carts[cart_id].append(product)
                return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.lock_add_remove:
            if product in self.carts[cart_id]:
                self.carts[cart_id].remove(product)
                self.queues[self.producers[product]] += 1
                self.products.append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        lst = self.carts[cart_id]
        del self.carts[cart_id]
        with self.lock_place_order:
            for product in lst:
                print(currentThread().getName() + " bought " + str(product))
        return lst
