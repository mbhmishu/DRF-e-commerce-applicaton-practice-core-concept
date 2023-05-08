from django.urls import path
from .views import CategoryList, CategoryDetail, ProductList, ProductDetail,ProductImgDetail,AttributeAPIView


app_name='shop_app'

urlpatterns = [
    path('categories/', CategoryList.as_view(),name='categories'),
    path('category-detail/<int:pk>/', CategoryDetail.as_view(),name='category_detail'),
    path('products-list/', ProductList.as_view(),name='Product_list'),
    path('products-list/<slug:slug>/', ProductDetail.as_view(),name='Product_list'),
    path('products-detail/<slug>/', ProductDetail.as_view(),name='product_details'),
    # path('product_img_detail/<int:pk>/', ProductImgDetail.as_view(),name='product_img_detail'),
    path('attributes/',AttributeAPIView.as_view(), name='attribute_list_create'),
    path('attributes/<int:pk>/', AttributeAPIView.as_view(), name='attribute_detail'),
]

