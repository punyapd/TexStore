from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from django.shortcuts import render
from rest_framework import status

from django.contrib.auth.hashers import make_password

from base.models import Order, Product, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItem(request):
    user = request.user
    data = request.data
   
    orderItems = data['orderItems']
    print( 'orderitems: ' , orderItems)
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'no order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # creating order

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            totalPrice=data['totalPrice'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],


        )

        # create shipping Address

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalcode'],
            country=data['shippingAddress']['country'],
        )

        # creating orderITems and realtionship between order and orderitem
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['qty'],
                price=i['price'],
                image=product.image.url,
            )

        # decrementing the countinstock

            product.countInStock -= int(item.quantity)
            product.save()

        serializer = OrderSerializer(order, many= False)
        
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request , pk):
    user = request.user

    order = Order.objects.get(_id = pk )

    try:
        if user.is_staff or order.user : 
            serializer = OrderSerializer(order , many = False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'you are not authorized!!!'} , status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'order not found'} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request , pk):
    
    order = Order.objects.get(_id = pk)
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('ORder is paid')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer( orders , many = True)
    return Response(serializer.data)


#VIEW FOR LSITIG THE ORDERS IN ADMIN PAGE

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    user = request.user
    orders = Order.objects.all()
    serializer = OrderSerializer( orders , many = True)
    return Response(serializer.data)



# VIE FOR UPDATING THE ORDER DELEVERY STATUS

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToDelivered(request , pk):
    
    order = Order.objects.get(_id = pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('ORder is delivered')