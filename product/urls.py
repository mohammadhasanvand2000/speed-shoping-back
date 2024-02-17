from django.urls import path,include
from .views import *





urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('grouping/', GroupingListView.as_view(), name='grouping'),
    path('detail/<int:id>/', CombinedView.as_view(), name='detail'),
    path('cart/', CartAPIView.as_view(), name='cart-view'),
    path('add-to-cart/<int:product_id>/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('favorites/<int:pk>/', AddToFavoriteView.as_view(), name='favorite-list-create'),
    path('favorites/<int:pk>/', FavoriteDestroyView.as_view(), name='favorite-destroy'),
    path('shipping-info/<int:cart_id>/', ShippingInfoAPIView.as_view(), name='shipping-info'),

    
    
]
