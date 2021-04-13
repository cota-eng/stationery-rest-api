from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('category',views.CategoryFilteredListAPIView)
router.register('brand',views.BrandFliteredListAPIView)
router.register('tag', views.TagFilteredProductListAPIView)
"""
below 3 view is not needed
"""
# router.register('product-category',views.ProductCategoryFilteredReadOnlyViewSet)
# router.register('product-brand',views.ProductBrandFilteredReadOnlyViewSet)
# router.register('product-tag', views.ProductTagFilteredReadOnlyViewSet)

"""
now unuse
"""
router.register('search', views.ProductSearchByName)
router.register('fav',views.FavProductAPIView)
router.register('review', views.ReviewViewSet)

app_name="pen"
urlpatterns = [
    path("category/<slug:category__slug>/brand/<slug:brand__slug>/",views.ProductCategoryBrandFilteredAPIView.as_view(),name="product-category"),
    path("category/<slug:brand__slug>/brand/<slug:category__slug>/",views.ProductCategoryBrandFilteredAPIView.as_view(),name="product-category"),
    # これと単純にサーチするもののどちらが早いか
    path("brand/<slug:brand__slug>/products",views.ProductBrandFilteredAPIView.as_view(),name="product-brand"),
    path("products/",views.ProductListAPIView.as_view(),name="product-list"),
    path("products/<str:pk>/",views.ProductRetrieveAPIView.as_view(),name="product"),
    path("fav-list/",views.OwnFavProductListAPIView.as_view(),name="fav-list"),
    path("review-list/",views.OwnReviewProductListAPIView.as_view(),name="review-list"),
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