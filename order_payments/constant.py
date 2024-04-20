STATUS_PENDING = 'Pending'
STATUS_COMPLETED = 'Completed'
STATUS_FAILED = 'Failed'
PAYMENT_TYPES_CARD = 'card'
PAYMENT_TYPES_CASH_ON_DELIVERY = 'cash_on_delivery'
STATUS_CHOICES = [
    (STATUS_PENDING, 'Pending'),
    (STATUS_COMPLETED, 'Completed'),
    (STATUS_FAILED, 'Failed'),
]

PAYMENT_TYPES_CHOICES = [
    (PAYMENT_TYPES_CARD, 'Card'),
    (PAYMENT_TYPES_CASH_ON_DELIVERY, 'cash_on_delivery'),
]
