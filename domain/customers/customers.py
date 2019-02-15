from eventsourcing.domain.model.aggregate import AggregateRoot


class Customer(AggregateRoot):
    def __init__(self, command_id=None, order_id=None, **kwargs):
        super(Customer, self).__init__(**kwargs)
        self.command_id = command_id
        self.is_blocked = False
        self.first_order_id = order_id
        self.orders = []

    def orders_count(self):
        return len(self.orders)

    class Event(AggregateRoot.Event):
        pass

    class Blocked(Event):
        def mutate(self, customer):
            customer.is_blocked = True

    class Unblocked(Event):
        def mutate(self, customer):
            customer.is_blocked = False

    class Ordered(Event):
        def mutate(self, customer):
            customer.orders.append(self.order_id)

    class FailedToOrder(Event):
        pass

    class Created(Event, AggregateRoot.Created):
        def __init__(self, **kwargs):
            super(Customer.Created, self).__init__(**kwargs)

    def block(self):
        self.__trigger_event__(Customer.Blocked)

    def unblock(self):
        self.__trigger_event__(Customer.Unblocked)

    def order(self, order_id):
        self.__trigger_event__(Customer.Ordered, order_id=order_id)

    def fail_to_order(self, order_id):
        self.__trigger_event__(Customer.FailedToOrder, order_id=order_id)
