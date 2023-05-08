from django.urls import path
from .views import AddToCartAPIView, CartView, RemoveFromCartView, IncreaseCartView

urlpatterns = [
    path('cart/add/<int:pk>/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/increase/<int:pk>/', IncreaseCartView.as_view(), name='increase-cart'),
]


