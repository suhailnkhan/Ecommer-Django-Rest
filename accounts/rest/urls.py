from django.urls import path
from accounts.rest.views import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView , CustomTokenObtainPairView , UserRolePermissions
urlpatterns = [
    path('users/customer/signup/', UserCreateAPIView.as_view(), name="create_customer_api"),
    path('users/customer/<uuid:pk>/details', UserRetrieveUpdateDestroyAPIView.as_view(), name="update_customer_api"),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('permissions/', UserRolePermissions.as_view(), name='token_obtain_pair'),
    
]