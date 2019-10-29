"""
   Author: Danny Barker
   Purpose: To convert rating data to json
   Methods: GET, POST
"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from emtapi.models import *
from .customer import CustomerSerializer



class StoreSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    merchant = CustomerSerializer(many=False)
    class Meta:
        model = Store
        url = serializers.HyperlinkedIdentityField(
            view_name='Store',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant', 'store_name', 'address_line_one', 'address_line_two', 'zip_code', 'description', 'created_date')
        depth = 1


class Store(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_store = Store()
        merchant = Customer.objects.get(user=request.auth.user)
        new_store.merchant = merchant
        new_store.store_name = request.data["store_name"]
        new_store.address_line_one = request.data["address_line_one"]
        new_store.address_line_two = request.data["address_line_two"]
        new_store.zip_code = request.data["zip_code"]
        new_store.description = request.data["description"]
        new_store.created_date = request.data["created_date"]
        new_store.save()

        serializer = StoreSerializer(new_store, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park Ratings resource

        Returns:
            Response -- JSON serialized list of park Ratings
        """
        store = Store.objects.all()

        serializer = StoreSerializer(
            store, many=True, context={'request': request})
        return Response(serializer.data)