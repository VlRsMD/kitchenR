## outcoming order builder
class orderOut:
    def __init__(self, order_id, table_id, waiter_id, priority, items, max_wait, pick_up_time, cooking_time, cooking_details):
        self.order_id = order_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.priority = priority
        self.items = items
        self.max_wait = max_wait
        self.pick_up_time = pick_up_time
        self.cooking_time = cooking_time
        self.cooking_details = cooking_details

## cooking details builder
class c_det:
    def __init__(self, food_item, cook_name):
        self.food_item = food_item
        self.cook_name = cook_name
