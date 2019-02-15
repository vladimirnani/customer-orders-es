# customer-orders-es

## Invariants
1. Orders should be canceled if customer is blocked
2. New order will try to create customer if no customer exist
3. Customer should have orders assigned to him
4. Unblocked customers are allowed to recieve orders
