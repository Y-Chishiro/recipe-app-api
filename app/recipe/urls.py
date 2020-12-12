from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()  # DRFの機能。自動でURLを割り当てる。
router.register('tags', views.TagViewSet)
# 何が嬉しいかというと、ViewSet側でURLを追加して行ったときに、
# したのurlpatternsを自動で更新してくれる。
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
