from eventsourcing.domain.model.aggregate import AggregateRoot


class Order(AggregateRoot):
    def __init__(self, command_id=None, phone=None, *args, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.command_id = command_id
        self.customer_id = None
        self.phone = phone

    class Event(AggregateRoot.Event):
        pass

    class Created(Event, AggregateRoot.Created):
        def __init__(self, **kwargs):
            super(Order.Created, self).__init__(**kwargs)

    class Canceled(Event):
        def mutate(self, order):
            order.canceled = True
            order.cancel_reason = self.reason
            order.customer_id = self.customer_id

    class CustomerAssigned(Event):
        def mutate(self, order):
            order.customer_id = self.customer_id

    def set_customer(self, customer_id):
        self.__trigger_event__(Order.CustomerAssigned,
                               customer_id=customer_id,
                               command_id=self.command_id)

    def cancel(self, reason, customer_id):
        self.__trigger_event__(Order.Canceled,
                               reason=reason,
                               command_id=self.command_id,
                               customer_id=customer_id)
