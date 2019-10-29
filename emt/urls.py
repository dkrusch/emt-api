from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from emtapi.models import *
from emtapi.views import *
# from emtapi.views import register_user, login_user

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', Customers, 'customer')
router.register(r'users', UserViewSet, 'user')
router.register(r'orders', Orders, 'order')
router.register(r'payments', Payments, 'payment')
router.register(r'stores', Store, 'store')
router.register(r'transactions', Transaction, 'order')
router.register(r'vendinfo', Vendinfo, 'vendinfo')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth$', obtain_auth_token),
    url(r'^api-auth$', include('rest_framework.urls', namespace='rest_framework')),
]
