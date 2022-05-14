from django.urls import path
from base.views import users_views as views

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
   
    path('profile/' , views.getUserProfile , name = "profile"),
    path('profile/update/' , views.updateUserProfile , name = "profile-update"),
    path('' , views.getUsers , name = "get_user"),
    path('delete/<str:pk>/' , views.deleteUser , name = "delete-user"),
    path('register/' , views.RegisterUser , name = "register"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

