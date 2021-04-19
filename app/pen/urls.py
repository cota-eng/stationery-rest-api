from django.urls import path,include
from rest_framework import routers
from . import views



router = routers.DefaultRouter()
"""
now unuse
"""
# router.register('search', views.ProductSearchByName)
# router.register('fav',views.FavProductAPIView)
# router.register('review', views.ReviewViewSet)

app_name="pen"
urlpatterns = [
    path("search/",views.ProductSearchByName.as_view(),name="search"),
    path("category/",views.CategoryListAPIView.as_view(),name="category-list"),
    path("brand/",views.BrandListAPIView.as_view(),name="brand-list"),
    path("tag/",views.TagListAPIView.as_view(),name="tag-list"),
    path("category/<slug:category__slug>/brand/<slug:brand__slug>/",views.ProductCategoryBrandFilteredAPIView.as_view(),name="product-category"),
    # path("category/<slug:brand__slug>/brand/<slug:category__slug>/",views.ProductCategoryBrandFilteredAPIView.as_view(),name="product-category"),
    # これと単純にサーチするもののどちらが早いか
    path("brand/<slug:brand__slug>/category/<slug:category__slug>/",views.ProductBrandCategoryFilteredAPIView.as_view(),name="product-brand"),
    path("products/",views.ProductListAPIView.as_view(),name="product-list"),
    path("products/<uuid:pk>/",views.ProductRetrieveAPIView.as_view(),name="product"),
    # path("fav-list/",views.OwnFavProductListAPIView.as_view(),name="fav-list"),
    # path("review-list/",views.OwnReviewProductListAPIView.as_view(),name="review-list"),
    path('',include(router.urls)),
]

"""
url memo

api/category/[category]/brand/[brand]
api/brand/[brand]/category/[category]

特定のカテゴリの商品一覧の中で、ブランドごとに分ける？
特定のブランドの商品一覧の中で、カテゴリごとに分ける？
タグ検索、タグの複数選択

"""