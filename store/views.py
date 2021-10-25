import collections
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from rest_framework import serializers
from rest_framework import pagination

from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView # base class of all api views
#from rest_framework.mixins import ListModelMixin, CreateModelMixin
#from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.filters import ProductFilter
from store.pagination import DefaultPagination

from .models import CartItem, Collection, OrderItem, Product, Review, Cart
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
#from rest_framework.pagination import PageNumberPagination

# using a viewset we can combine logic for multiple related views inside in sigle class
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = [ 'unit_price', 'last_update' ]
    pagination_class = DefaultPagination
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id',None)
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)

    #     return queryset

    def get_serializer_context(self):
        return { 'request' : self.request }

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter( product_id = kwargs['pk'] ).count() > 0:
             return Response({'error': 'Product cannot be deleted becasue it is associated with an order item' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delet(self, request,pk):
    #     product = get_object_or_404( Product, pk=pk )
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted becasue it is associated with an order item' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


"""class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    #def get_queryset(self):
    #    return Product.objects.select_related('collection').all()
    
    #def get_serializer(self, *args, **kwargs):
    #    return ProductSerializer
    
    def get_serializer_context(self):
        return { 'request' : self.request }"""


"""class ProductList(APIView):
    def get(self, request):
        querySet = Product.objects.select_related('collection').all()
        serializers = ProductSerializer(querySet, many=True, context = {'request':request})
        return Response(serializers.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
"""


"""@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        querySet = Product.objects.select_related('collection').all()
        serializers = ProductSerializer(querySet, many=True, context = {'request':request})
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        #if serializer.is_valid(): # serializer.is_valid(raise_exception=True)
        #    serializer.validated_data
        #    return Response('OK')
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """

"""class ProductDetail(RetrieveUpdateDestroyAPIView):  # changed from APIView to RetrieveUpdateDestroyAPIView
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #lookup_field = 'id'

    #def get(self, request, id):
    #    product = get_object_or_404( Product, pk=id )
    #    serializers = ProductSerializer( product, context = {'request':request} )
    #    return Response(serializers.data)

    #def put(self, request,id):
    #    product = get_object_or_404( Product, pk=id )
    #    serializer = ProductSerializer(product, data=request.data)
    #    serializer.is_valid(raise_exception =True )
    #    serializer.save()
    #    return Response(serializer.data)

    def delete(self, request,pk):
        product = get_object_or_404( Product, pk=pk )
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted becasue it is associated with an order item' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

class CollectionViewSet(ModelViewSet):  # ReadOnlyModelViewSet
    queryset = Collection.objects.annotate(products_count = Count('products') ).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404( Collection, pk = kwargs['pk'] )
        if collection.products.count() > 0:
             return Response({'error': 'Collection cannot be deleted becasue it includes one or more products' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404( Collection, pk = pk )
    #     if collection.products.count > 0:
    #         return Response({'error': 'Collection cannot be deleted becasue it includes one or more products' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)




"""
@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404( Product, pk=id )
    if request.method == 'GET':
        serializers = ProductSerializer( product, context = {'request':request} )
        return Response(serializers.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception =True )
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted becasue it is associated with an order item' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products') ).all()
    serializer_class = CollectionSerializer"""


"""@api_view( ['GET','POST'] )
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count = Count('products') ).all()
        serializer = CollectionSerializer(queryset, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer( data = request.data )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED )
"""

"""class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate( product_count = Count('products') )
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404( Collection, pk = pk )
        if collection.products.count > 0:
            return Response({'error': 'Collection cannot be deleted becasue it includes one or more products' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


"""@api_view(['GET','PUT','DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
            Collection.objects.annotate( product_count = Count('products') ),
            pk=pk
        )
    if request.method == 'GET':
        serializer = CollectionSerializer( collection, context = { 'request' : request } )
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer( collection, data= request.data )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count > 0:
            return Response({'error': 'Collection cannot be deleted becasue it includes one or more products' } , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class ReviewViewSet(ModelViewSet):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return { 'product_id': self.kwargs['product_pk'] }

class CartViewSet(CreateModelMixin,
                    RetrieveModelMixin,
                    DestroyModelMixin, 
                    GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return { 'cart_id':self.kwargs['cart_pk'] }

    def get_queryset(self):
        print(self.kwargs)
        return CartItem.objects.prefetch_related('product').filter(cart_id = self.kwargs['cart_pk'])