"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from emtapi.models import *
from .customer import CustomerSerializer
from .store import StoreSerializer


'''
auther: Tyler Carpenter
purpose: Allow a user to communicate with the emt database to GET PUT POST and DELETE entries.
methods: all
'''

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order

    Arguments:
        serializers
    """

    customer = CustomerSerializer(many=False)
    store = StoreSerializer(many=False)

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer', 'store', 'payment_type', 'vend_amount', 'denomination', 'created_date', 'time_complete')
        depth = 1


class Orders(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        new_order = Order()
        customer = Customer.objects.get(id=request.data["customer_id"])
        new_order.customer = customer
        store = Store.objects.get(id=request.data["store_id"])
        new_order.store = store
        new_order.payment_type = Payment.objects.get(id=request.data["payment_type"])
        new_order.vend_amount = request.data["vend_amount"]
        new_order.denomination = request.data["denomination"]
        new_order.created_date = request.data["created_date"]
        # new_order.time_complete = request.data["time_complete"]
        new_order.save()

        serializer = OrderSerializer(new_order, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for order

        Returns:
            Response -- JSON serialized order
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.time_complete = request.data["time_complete"]
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        orders = Order.objects.all()

        merchant = self.request.query_params.get('merchant', None)
        complete = self.request.query_params.get('complete', None)

        if merchant is not None:
            orders = orders.filter(store__merchant__id=merchant)
        if complete is not None:
            if complete == "1":
                orders = orders.filter(time_complete__isnull=False)
            elif complete == "0":
                orders = orders.filter(time_complete__isnull=True)

        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)
