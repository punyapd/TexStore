from asyncio.windows_events import NULL
from math import prod
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


from django.views.decorators.csrf import csrf_protect

from django.views.decorators.csrf import csrf_exempt
 

from django.shortcuts import render

from django.contrib.auth.hashers import make_password
from base.models import Review
from base.models import Product
from base.serializers import ProductSerializer


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('search')
   
    if query  ==  None:
        query = ''
      
     
    products = Product.objects.filter(name__icontains = query)
     
    
       
        

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


#view for deleting product from admin 
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response("product is deleted")

#view for creating product from admin
@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user

    product = Product.objects.create(
        user=user,
        name = "sample product",
        brand = " sample brand",
        category = " c",
        price=300,
        countInStock=0,
        description='this is a smaple product')


    serializer=ProductSerializer(product, many=False)
    return Response(serializer.data)

#view for updating product details from admin
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request , pk):
    user = request.user
    data = request.data
    # print(data['price'])
    product = Product.objects.get(_id = pk)
   
    product.name = data['name']
    product.category =data['category']
    product.brand = data['brand']
    product.price=data['price']
    product.countInStock=data['countInStock']
    product.description=data['description']

    product.save()


    serializer=ProductSerializer(product, many=False)
    return Response(serializer.data)

#VIEW FOR UPLOADING THE IMAGE FROM FRONTEND
@csrf_exempt
@api_view(['POST'])
def imageUpload(request):
    data = request.data 

    prod_id = data['product_id']
    product = Product.objects.get(_id = prod_id)

    product.image = request.FILES.get('image')

    product.save()
    return Response("image was successfully uploaded. ")


#VIEW FOR POSTING THE REVIEWS

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request , pk):
    user = request.user
    product = Product.objects.get(_id = pk)
    data = request.data 

    #chek if review already exists
    alreadyExists = product.review_set.filter( user = user).exists()

    if(alreadyExists):
        content = {'detail' : 'Product alreay reviewed'}
        return Response(content , status=status.HTTP_400_BAD_REQUEST)
    #CREATE REVIEW
    else:
        review = Review.objects.create(
          user = user,
          product = product,
          name = user.first_name , 
          rating = data['rating'],
          comment = data['comment']
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)


        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total/len(reviews)
        product.save()

        return Response("review added")



#VIEW FOR GETTING PRODUCTS FOR CAROUSEL

@api_view(['GET'])
def getTopProduct(request):
    product = Product.objects.filter(rating__gte = 4).order_by('-rating')[0:5]
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

   
   
    


   
    





