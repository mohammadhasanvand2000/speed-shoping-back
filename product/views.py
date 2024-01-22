from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from .serializers import *

from rest_framework import generics
from .models import *
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class GroupingListView(generics.ListAPIView):
    queryset = Grouping.objects.all()
    serializer_class = GroupingSerializer
    permission_classes = [permissions.AllowAny]




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class CombinedView(APIView):
    serializer_class = CombinedSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            detail = get_object_or_404(Detail, producti=id)
            product_image = Product_image.objects.filter(producti__id__exact=id)
            product_colors = Product_color.objects.filter(producti=id)
            

            combined_data = {
                'product': product,
                'detail': detail,
                'product_image': product_image,
                'product_color': product_colors,
                
            }

            # ساخت نمونه از سریالایزر
            serializer = self.serializer_class(combined_data)

            # برگرداندن JSON حاوی اطلاعات
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



from .serializers import CartSerializer

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        serializer = CartSerializer(cart_items, many=True)
        cart_data = serializer.data

        return Response({'cart': cart_data})

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()

        return Response({'success': True}, status=status.HTTP_201_CREATED)

class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is in the cart
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

        return Response({'success': True}, status=status.HTTP_200_OK)
