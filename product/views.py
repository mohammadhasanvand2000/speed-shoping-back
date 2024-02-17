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






from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Serialize the cart data
        serializer = CartSerializer(cart)
        cart_data = serializer.data

        # Retrieve additional product details for each cart item
        detailed_cart_items = []
        for cart_item in cart_items:
            product_id = cart_item.product.id
            product = get_object_or_404(Product, id=product_id)  # Replace 'Product' with your actual product model
            product_data = ProductSerializer(product).data

            cid={'cart_id': cart.id}
            detailed_cart_item = {
                
                
                'cart_item': CartItemSerializer(cart_item).data,
                'product_details': product_data,
            }

            detailed_cart_items.append(detailed_cart_item)

        cart_data['detailed_cart_items'] = detailed_cart_items

        return Response({'cid': cid,'cart': cart_data})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product
from .serializers import CartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product
from .serializers import CartItemSerializer

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            # Extract quantity and color from request.data
            quantity = int(request.data.get('quantity', 1))
            color = request.data.get('color', '')

            # Get or create cart for the current user
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Get the product
            product = get_object_or_404(Product, id=product_id)

            # Check if the product is already in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color)

            # Update quantity and save
            cart_item.quantity = quantity
            cart_item.save()

            # Serialize the cart item
            serializer = CartItemSerializer(cart_item)

            return Response({'success': True, 'cart_item': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, product_id):
        try:
            # Extract quantity from request.data
            quantity = int(request.data.get('quantity', 1))

            # Get the cart item
            cart_item = get_object_or_404(CartItem, cart__user=request.user, product__id=product_id)

            # Update quantity and save
            cart_item.quantity = quantity
            cart_item.save()

            # Serialize the updated cart item
            serializer = CartItemSerializer(cart_item)

            return Response({'success': True, 'cart_item': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    

class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is in the cart
        cart_item =  get_object_or_404(CartItem, cart=cart, product=product)
        

       
        cart_item.delete()
      
        return Response({'success': True}, status=status.HTTP_200_OK)






from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Favorite
from .serializers import FavoriteSerializer
from rest_framework.permissions import IsAuthenticated


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(id=pk)

        # چک کردن وجود محصول در لیست علاقه‌مندی‌ها
     
            # اگر محصول در لیست نباشد، اضافه کنید
        Favorite.objects.create(user=user, product=product)
        return Response({'success': True, 'message': 'محصول به لیست علاقه‌مندی اضافه شد.'}, status=status.HTTP_201_CREATED)
       
class FavoriteDestroyView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    











    
class ShippingInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, cart_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        shipping_infos = ShippingInfo.objects.filter(cart__id=cart_id)
        serializer = ShippingInfoSerializer(shipping_infos, many=True)
        return Response(serializer.data)

    def post(self, request, cart_id):
        serializer = ShippingInfoSerializer(data=request.data)
        if serializer.is_valid():
            cart = Cart.objects.get(id=cart_id)
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)