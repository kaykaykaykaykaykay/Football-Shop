from django.urls import path
from .views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_product, delete_product, ajax_login, ajax_register, ajax_create_product, ajax_edit_product, ajax_delete_product, ajax_logout

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path("create-product/", create_product, name="create_product"),
    path("ajax-create-product/", ajax_create_product, name="ajax_create_product"),
    path("product/<uuid:id>/", show_product, name="show_product"),
    path("product/<uuid:id>/edit/", edit_product, name="edit_product"),
    path("ajax-product/<uuid:id>/edit/", ajax_edit_product, name="ajax_edit_product"),
    path("product/<uuid:id>/delete/", delete_product, name="delete_product"),
    path("ajax-product/<uuid:id>/delete/", ajax_delete_product, name="ajax_delete_product"),
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<uuid:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<uuid:id>/", show_json_by_id, name="show_json_by_id"),
    path('register/', register, name='register'),
    path('ajax-register/', ajax_register, name='ajax_register'),
    path('login/', login_user, name='login'),
    path('ajax-login/', ajax_login, name='ajax_login'),
    path('logout/', logout_user, name='logout'),
    path('ajax-logout/', ajax_logout, name='ajax_logout'),
]