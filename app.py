from eventsourcing.application.system import System

# os.environ['DB_URI'] = 'sqlite:///orders.db'
from domain.commands import Commands
from domain.customers.process import Customers
from domain.orders.process import Orders

system = System(
    Commands | Orders | Customers | Orders | Commands
)
system.setup_tables = True

with system:
    cmd_id = system.commands.create_new_order(phone='1234')
    command = system.commands.repository[cmd_id]
    order = system.orders.repository[command.order_id]
    customer_id = order.customer_id

    customer = system.customers.repository[customer_id]
    assert customer.orders_count() == 1

    customer.block()

    assert customer.is_blocked
    customer.__save__()

    system.commands.create_new_order(phone='1234')
    assert customer.orders_count() == 1

    customer = system.customers.repository[customer_id]
    customer.unblock()

    assert not customer.is_blocked
    customer.__save__()

    system.commands.create_new_order(phone='1234')
    customer = system.customers.repository[customer_id]
    assert customer.orders_count() == 2
