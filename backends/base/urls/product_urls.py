from django.urls import path
from base.views import product_views as views



urlpatterns = [
   
    path('' , views.getProducts , name = "product"),
    path('create/' , views.createProduct , name = 'createProduct') , 
    path('upload/' , views.imageUpload , name = 'image-upload') , 
    path('topproducts/' , views.getTopProduct , name = 'top-Product') ,
    path('<str:pk>/reviews/' , views.createProductReview , name = 'create-review'),
    path('update/<str:pk>/' , views.updateProduct , name = "update-product"),
    path('<str:pk>/' , views.getProduct , name = "product"),
    path('delete/<str:pk>/' , views.deleteProduct , name = "delete_product")
    
]

