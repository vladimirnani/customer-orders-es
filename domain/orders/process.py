from eventsourcing.application.sqlalchemy import ProcessApplication

from domain.commands import CreateNewOrder
from domain.customers.customers import Customer
from domain.orders.orders import Order


class Orders(ProcessApplication):
    @staticmethod
    def policy(repository, event):
        if isinstance(event, CreateNewOrder.Created):
            return Order.__create__(command_id=event.originator_id, phone=event.phone)

        if isinstance(event, Customer.Ordered):
            order = repository[event.order_id]
            order.set_customer(event.originator_id)

        if isinstance(event, Customer.FailedToOrder):
            order = repository[event.order_id]
            order.cancel(reason='Customer is blocked', customer_id=event.originator_id)
