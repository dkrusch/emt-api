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
from .store import StoreSerializer
from .order import OrderSerializer



class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    store = StoreSerializer(many=False)
    order = OrderSerializer(many=False)
    class Meta:
        model = Transaction
        url = serializers.HyperlinkedIdentityField(
            view_name='Transaction',
            lookup_field='id'
        )
        fields = ('id', 'url', 'store', 'order', 'time_complete')
        depth = 1

class Transaction(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product transaction instance
        """
        new_transaction = Transaction()
        store = Store.objects.get(pk=request.data["store_id"])
        new_transaction.store = store
        order = Order.objects.get(pk=request.data["order_id"])
        new_transaction.order = order
        new_transaction.time_complete = request.data["time_complete"]
        new_transaction.save()

        serializer = TransactionSerializer(new_transaction, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            transaction = Transaction.objects.get(pk=pk)
            serializer = TransactionSerializer(transaction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park Ratings resource

        Returns:
            Response -- JSON serialized list of park Ratings
        """
        transactions = Transaction.objects.all()

        serializer = TransactionSerializer(
            transactions, many=True, context={'request': request})
        return Response(serializer.data)