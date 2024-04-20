from accounts.constants import ADMIN_ROLE,CUSTOMER_ROLE,SHOP_ADMIN_ROLE,SUPER_ADMIN_ROLE
from accounts.permission_constants import BLINKBUY_ADMIN ,BLINKBUY_CUSTOMER , BLINKBUY_SHOP_ADMIN  , BLINKBUY_SUPER_ADMIN


def salutation_choices():
    choices = (('Mr', 'Mr'), ('Ms', 'Ms'),)
    return choices



def get_user_role_permission(user_role):
    if user_role == CUSTOMER_ROLE:
        return BLINKBUY_CUSTOMER
    if user_role == SHOP_ADMIN_ROLE:
        return BLINKBUY_SHOP_ADMIN
    if user_role == ADMIN_ROLE:
        return BLINKBUY_ADMIN
    if user_role == SUPER_ADMIN_ROLE:
        return BLINKBUY_SUPER_ADMIN
    return None
