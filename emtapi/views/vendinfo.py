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
from .vendinfo import VendInfo
from .store import StoreSerializer


class VendinfoSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    store = StoreSerializer(many=False)

    class Meta:
        model = VendInfo
        url = serializers.HyperlinkedIdentityField(
            view_name='Vendinfo',
            lookup_field='id'
        )
        fields = ('id', 'url', 'store', 'start_time', 'end_time', 'vend_limit')
        depth = 1


class Vendinfo(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product Vendinfo instance
        """
        new_vendinfo = Vendinfo()
        store = Store.objects.get(pk=request.data["store_id"])
        new_vendinfo.store = store
        new_vendinfo.start_time = request.data["start_time"]
        new_vendinfo.end_time = request.data["end_time"]
        new_vendinfo.vend_limit = request.data["vend_limit"]
        new_vendinfo.save()

        serializer = VendinfoSerializer(new_vendinfo, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            Vendinfo = Vendinfo.objects.get(pk=pk)
            serializer = VendinfoSerializer(Vendinfo, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park Ratings resource

        Returns:
            Response -- JSON serialized list of park Ratings
        """
        Vendinfos = Vendinfo.objects.all()

        serializer = VendinfoSerializer(
            Vendinfos, many=True, context={'request': request})
        return Response(serializer.data)