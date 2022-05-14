from django.urls import path
from base.views import order_views as views

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
   path('addorder/' , views.addOrderItem , name = "add-order"),
   path('myorders/' , views.getMyOrders , name = 'my-orders'),
   path('<str:pk>/' , views.getOrderById , name = 'user_order'),
   path('<str:pk>/pay/' , views.updateOrderToPaid , name = 'pay-order'),
   
]
