from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/<str:obj_alias>/<str:obj_target>", views.create, name="create"),
    path("get/<str:obj_alias>", views.get, name="get"),
    path("get_on_date/<str:obj_alias>/<str:on_date>", views.get_on_date, name="get_on_date"),
    path("aliases/<str:alias_target>/<str:from_datetime>/<str:to_datetime>", views.aliases, name="aliases"),
    path("replace/<str:existing_alias>/<str:alias_start>/<str:new_alias_value>",
         views.replace, name="replace")
]
