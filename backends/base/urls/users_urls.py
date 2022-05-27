from django.urls import path
from base.views import users_views as views

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/' , views.getUserProfile , name = "profile"),
    path('profile/update/' , views.updateUserProfile , name = "profile-update"),
   
    path('' , views.getUsers , name = "get_user"),
    path('<str:pk>/' , views.getUserById , name = 'get-suer-by-id'),
    path('update/<str:pk>' , views.updateUser , name = 'update-user'),
    path('delete/<str:pk>/' , views.deleteUser , name = "delete-user"),
    path('register/' , views.RegisterUser , name = "register"),
   
]
