from django.urls import path
from .views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, add_employee

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path("create-product/", create_product, name="create_product"),
    path("product/<uuid:id>/", show_product, name="show_product"),
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<uuid:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<uuid:id>/", show_json_by_id, name="show_json_by_id"),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_employee', add_employee,name='add_employee' ),
]