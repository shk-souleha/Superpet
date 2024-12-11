from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(),name="products"),
    path('royal-canin/',views.royalCanin,name="royalcanin"),
    path('drools/',views.drools,name="drools"),
    path('search',views.search,name="search"),
    path('<int:pk>/',views.ProductDetailView.as_view(),name="product-detail"),
    path('create-product/',views.ProductCreateView.as_view(),name="create-product"),
    path('update-product/<int:pk>/',views.ProductUpdateView.as_view(),name="update-product"),
    path('delete-product/<int:pk>/',views.ProductDeleteView.as_view(),name="delete-product"),
    path('<slug:slug>/',views.CategoryDetailView.as_view(),name="category-detail")
]