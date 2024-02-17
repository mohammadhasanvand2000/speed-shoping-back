from rest_framework import serializers
from .models import *


class GroupingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grouping
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_image
        fields = '__all__'



class ProductColorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product_color
        fields = '__all__'




class ClientComentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Coments
        fields = '__all__'






        

class CombinedSerializer(serializers.Serializer):
    product = ProductSerializer()
    detail = DetailSerializer()
    product_image = ProductImageSerializer(many=True)
    product_color = ProductColorSerializer(many=True)
    

   

    def to_representation(self, instance):
        # اگر instance['details'] یک لیست با یک عنصر از نوع Detail باشد، آن را به شیء تبدیل کنید
        if 'details' in instance and isinstance(instance['details'], list) and len(instance['details']) == 1:
            instance['details'] = instance['details'][0]

        # به تابع اصلی ادامه دهید
        representation = super().to_representation(instance)
        return representation

class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()

    def get_cart_items(self, cart):
        cart_items = CartItem.objects.filter(cart=cart)
        return CartItemSerializer(cart_items, many=True).data

    class Meta:
        model = Cart
        fields = ['user', 'items', 'cart_items']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity','color']




from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product']




class ShippingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = '__all__'