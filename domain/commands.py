from eventsourcing.application.sqlalchemy import CommandProcess
from eventsourcing.domain.model.command import Command
from eventsourcing.domain.model.decorators import attribute, retry
from eventsourcing.exceptions import OperationalError, RecordConflictError

from domain.orders.orders import Order


class CreateNewOrder(Command):
    def __init__(self, phone=None, **kwargs):
        super(CreateNewOrder, self).__init__(**kwargs)
        self.phone = phone

    class Created(Command.Created):
        pass

    @attribute
    def order_id(self):
        pass


class Commands(CommandProcess):
    @staticmethod
    def policy(repository, event):
        if isinstance(event, Order.Created):
            cmd = repository[event.command_id]
            cmd.order_id = event.originator_id
        elif isinstance(event, Order.Canceled) or isinstance(event, Order.CustomerAssigned):
            cmd = repository[event.command_id]
            cmd.done()

    @staticmethod
    @retry((OperationalError, RecordConflictError), max_attempts=10, wait=0.01)
    def create_new_order(phone):
        cmd = CreateNewOrder.__create__(phone=phone)
        cmd.__save__()
        return cmd.id
