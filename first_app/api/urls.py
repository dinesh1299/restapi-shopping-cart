from django.urls import path,include
from .views import *
from rest_framework.routers import *

router = DefaultRouter()
router.register('product',Product_ViewSet,basename="product")
urlpatterns = [
    path('category_list', GetCategories.as_view(), name='category-list'),
    path('get_category/<int:id>',GetCategory.as_view(),name="category-detail"),
    path('',include(router.urls)),
    path('product_list', GetProducts.as_view(), name='product-list'),
    path('get_product/<int:id>',GetProduct.as_view(),name="product-detail"),
    # path('<int:pk>/order_list',OrderList.as_view(),name='order-list'),
    path('order_list',OrderList.as_view(),name='order-list'),
    # path('order_create/<int:pk>',OrderCreate.as_view(),name='order-create'),
    path('order_update/<int:pk>',OrderUpdate.as_view(),name='order-update'),
    path('order_create',OrderCreate.as_view(),name='ordercreate'),
    
    path('get_order/<int:pk>',OrderDetail.as_view(),name='order-detail'),
    path('rating_list',RatingList.as_view(),name='rating-list'),
    path('create_rating/<int:pk>',RatingCreate.as_view(),name="rating-create"),
    path('get_rating/<int:id>',RatingDetail.as_view(),name='rating-detail'),
    path('rating_detail',UserRatingDetail.as_view(), name="user-rating-detail"),

    path('product_filter',ProductDetailFilter.as_view(), name='product-filter'),
    path('product_search',ProductDetailSearch.as_view(), name='product-search'),
    path('product_ordering',ProductDetailOrdering.as_view(), name='product-ordering'),

] 
