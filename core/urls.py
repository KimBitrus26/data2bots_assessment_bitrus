from django.urls import path
from .views import (ListProductsView, ListsCategoriesView, DetailProductView,
                    ListsProductsByCategoryView, SearchView, OrderView, OrderHistoryView)

urlpatterns = [
    path('products/', ListProductsView.as_view(), name='products'),
    path('categories/', ListsCategoriesView.as_view(), name="categories"),
    path('product-detail/<str:slug>/', DetailProductView.as_view(), name="product-detail"),
    path('products/<str:category_slug>/category/', ListsProductsByCategoryView.as_view(), name="products-category"),
    path('search', SearchView.as_view(), name="search"),
    path('order/<str:product_slug>/', OrderView.as_view(), name="order"),
    path('order-history/', OrderHistoryView.as_view(), name="order-history"),

]

