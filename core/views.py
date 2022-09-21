from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import  generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from assessment.pagination import StandardResultsSetPagination
from .models import Product, Category, Order
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer


class ListProductsView(generics.ListAPIView):
    """View to lists all products."""

    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ("get",)


class DetailProductView(generics.RetrieveAPIView):
    """View to get a single Product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    lookup_field = "slug"
    http_method_names = ("get",)


class ListsCategoriesView(generics.ListAPIView):
    """View to list categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ("get",)


class ListsProductsByCategoryView(generics.ListAPIView):
    """View to list Products by Category"""

    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ("get",)

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get("category_slug"))


class SearchView(APIView):
    """View to search for products."""

    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("query")
        if query:
            products = Product.objects.select_related("category", "price").filter(
                Q(title__icontains=query)
                | Q(category__title__icontains=query)).distinct()
            if products:
                serializer = ProductSerializer(products, many=True)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Search not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "Something went wrong. Try again."}, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    """View to order product."""

    permission_classes = (IsAuthenticated,)
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['product_slug'])
        order = Order.objects.create(
                                    user=request.user,
                                    product=product
                                    )
        serializer = OrderSerializer(order, many=False)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)


class OrderHistoryView(generics.ListAPIView):
    """View to get order history of a user."""

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ("get",)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
