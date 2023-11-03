from rest_framework.generics import  RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, CreateAPIView

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

class OwnerCreate(LoginRequiredMixin, CreateAPIView):
    """
    Sub-class the ListCreateAPIView to pass the request to the form and limit the
    queryset to the requesting user.
    """
    
class OwnerList(LoginRequiredMixin, ListAPIView):
    """
    Sub-class the ListCreateAPIView to pass the request to the form and limit the
    queryset to the requesting user.
    """


class OwnerDetailView(LoginRequiredMixin,RetrieveAPIView):
    
    """
    Sub-class the RetrieveAPIView to pass the request to the form and limit the
    queryset to the requesting user.
    """



class OwnerUpdateView(LoginRequiredMixin, UpdateAPIView):
    """
    Sub-class the UpdateAPIView to pass the request to the form and limit the
    queryset to the requesting user.
    """


class OwnerDeleteView(LoginRequiredMixin, DestroyAPIView):
    """
    Sub-class the DestroyAPIView to pass the request to the form and limit the
    queryset to the requesting user.
    """

class OwnerView(LoginRequiredMixin, APIView):
        """
    Sub-class the APIView to pass the request to the form and limit the
    queryset to the requesting user.
    """

