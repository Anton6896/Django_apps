from uuid import uuid4


def unique_order_id_generator(instance, num=0):
    """
    must have order_id field
    """
    order_new_id = str(uuid4()).upper()[:10] + str(num)

    klass = instance.__class__
    qs_exists = klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        num += 1
        return unique_order_id_generator(instance, num)
    return order_new_id
