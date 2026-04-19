from django.urls import path

from .views import (
    admin_dashboard,
    home,
    item_close,
    item_create,
    item_delete,
    item_detail,
    item_edit,
    my_items,
)

urlpatterns = [
    path("", home, name="home"),
    path("items/<int:pk>/", item_detail, name="item_detail"),
    path("items/new/", item_create, name="item_create"),
    path("items/<int:pk>/edit/", item_edit, name="item_edit"),
    path("items/<int:pk>/delete/", item_delete, name="item_delete"),
    path("items/<int:pk>/close/", item_close, name="item_close"),
    path("me/items/", my_items, name="my_items"),
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
]
