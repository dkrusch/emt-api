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
        fields = ('id', 'url', 'merchant', 'store_name', 'address_line_one', 'address_line_two', 'zip_code', 'description', 'created_date', 'start_time', 'end_time', 'vend_limit')
        depth = 1

class Stores(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_store = Store()
        merchant = Customer.objects.get(id=request.data["merchant_id"])
        new_store.merchant = merchant
        new_store.store_name = request.data["store_name"]
        new_store.address_line_one = request.data["address_line_one"]
        new_store.address_line_two = request.data["address_line_two"]
        new_store.zip_code = request.data["zip_code"]
        new_store.description = request.data["description"]
        new_store.created_date = request.data["created_date"]
        new_store.start_time = request.data["start_time"]
        new_store.end_time = request.data["end_time"]
        new_store.vend_limit = request.data["vend_limit"]
        new_store.save()

        serializer = StoreSerializer(new_store, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        update_store = Store.objects.get(pk=pk)
        # update_store.store_name = request.data["store_name"]
        # update_store.address_line_one = request.data["address_line_one"]
        # update_store.address_line_two = request.data["address_line_two"]
        # update_store.zip_code = request.data["zip_code"]
        # update_store.description = request.data["description"]
        # update_store.created_date = request.data["created_date"]
        update_store.start_time = request.data["start_time"]
        update_store.end_time = request.data["end_time"]
        update_store.vend_limit = request.data["vend_limit"]
        update_store.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
        stores = Store.objects.all()

        merchant = self.request.query_params.get('merchant', None)

        if merchant is not None:
            stores = stores.filter(merchant__id=merchant)

        serializer = StoreSerializer(
            stores, many=True, context={'request': request})
        return Response(serializer.data)



        # serializer = VendinfoSerializer(
        #     vendinfos, many=True, context={'request': request})
        # return Response(serializer.data)