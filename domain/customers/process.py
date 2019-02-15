import uuid

from eventsourcing.application.sqlalchemy import ProcessApplication

from domain.customers.customers import Customer
from domain.orders.orders import Order


class Customers(ProcessApplication):
    persist_event_type = Customer.Event

    @staticmethod
    def policy(repository, event):
        if isinstance(event, Order.Created):
            order_id = event.originator_id
            customer_id = uuid.uuid5(uuid.NAMESPACE_URL, event.phone)
            try:
                customer = repository[customer_id]
            except KeyError:
                customer = Customer.__create__(originator_id=customer_id, order_id=order_id)

            if not customer.is_blocked:
                customer.order(order_id)
            else:
                customer.fail_to_order(order_id)

            return customer
