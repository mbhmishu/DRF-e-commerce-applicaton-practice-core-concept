from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ShopApp.paginations import ProductSmallesetPagination
from rest_framework.filters import SearchFilter

from .models import Category, Product, ProductImg,ImgConnector, Tag, TagConnector,Attribute
from .serializers import CategorySerializer, ProductSerializer, ProductImgSerializer,TagSerializer,ImgConnectorSerializer,AttributeSerializer




class CategoryList(APIView):
    pagination_class = ProductSmallesetPagination
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        categories = Category.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(categories, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

        
    def post(self, request, format=None):
        #user must be a staff or admin
        # if not request.user.is_authenticated or not request.user.is_staff:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class CategoryDetail(APIView):
    def get_category(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        # if not request.user.is_authenticated or not request.user.is_staff:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        category = self.get_category(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # if not request.user.is_authenticated or not request.user.is_staff:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        category = self.get_category(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
#Product views

class ProductList(APIView):
    pagination_class = ProductSmallesetPagination
    serializer_class = ProductSerializer 
    filter_backends = [SearchFilter]
    search_fields = ['name','category']

    def get(self, request):
        products = Product.objects.all()
        print("d ", products)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        search_query = self.request.query_params.get('search', None)


        if min_price is not None and max_price is not None:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price is not None:
            products = products.filter(price__gte=min_price)
        elif max_price is not None:
            products = products.filter(price__lte=max_price)

        elif search_query is not None:
            queryset = queryset.filter(name__icontains=search_query) | queryset.filter(category__icontains=search_query)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(products, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
        


    def post(self, request):
        # if not request.user.is_authenticated or not request.user.is_staff:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        


class ProductDetail(APIView):
    def get_product(self,slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        product = self.get_product(slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, slug):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        product = self.get_product(slug)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        product = self.get_product(slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


 
############
class AttributeAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            try:
                attribute = Attribute.objects.get(pk=pk)
                serializer = AttributeSerializer(attribute)
            except Attribute.DoesNotExist:
                return Response({'error': 'Attribute does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            attributes = Attribute.objects.all()
            serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            attribute = Attribute.objects.get(pk=pk)
        except Attribute.DoesNotExist:
            return Response({'error': 'Attribute does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AttributeSerializer(attribute, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            attribute = Attribute.objects.get(pk=pk)
        except Attribute.DoesNotExist:
            return Response({'error': 'Attribute does not exist'}, status=status.HTTP_404_NOT_FOUND)
        attribute.delete()
        return Response({'message': 'Attribute deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#img Details view
class ProductImgDetail(APIView):
    
    def get_productimg(self, pk):
        try:
            return ProductImg.objects.get(pk=pk)
        except ProductImg.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        productimg = self.get_productimg(pk)
        serializer = ProductImgSerializer(productimg, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        productimg = self.get_productimg(pk)
        productimg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

