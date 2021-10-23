import collections
from django.db.models import fields
from django.db.models.base import Model
from django.db.models.query import QuerySet
from rest_framework import serializers

from decimal import Decimal

from store.models import Cart, Product, Collection, Review

""" Serialiazing relationships 
Primary key
String
Nested object
Hyperlink
 """

class CollectionSerializer(serializers.ModelSerializer):  # serializers.Serializer 
    class Meta:
        model = Collection
        fields = ['id','title', 'products_count' ]

    products_count = serializers.IntegerField(read_only = True)

    #id = serializers.IntegerField()
    #title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']    
    #id = serializers.IntegerField()
    #title = serializers.CharField(max_length=255)
    #price  = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculated_tax')
    #collection = serializers.StringRelatedField()
    #collection = serializers.PrimaryKeyRelatedField(
    #    queryset=Collection.objects.all()
    #)
    #collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #    queryset = Collection.objects.all(),
    #    view_name= 'collection-detail'
    #)


    def calculated_tax(self, product : Product):
        return product.unit_price * Decimal(1.1)
    
    #def validate(self, data):
    #    if data['password'] != data['confirm_password']:
    #        return serializers.ValidationError('Password do not match')

    # save method internally call create and update depending on data
    #def create(self, validated_data):
    #    product = Product(**validated_data)
    #    product.other = 1
    #    product.save()
    #    return product

    #def update(self, instance, validated_data):
    #    instance.unit_price = validated_data.get('unit_price')
    #    instance.save()
    #    return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [ 'id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id']