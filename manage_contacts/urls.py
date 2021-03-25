from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_contacts, name='manage_contacts'),
    # path('get_current_user', views.get_current_user, name="get_current_user"),

    path('add-contact', views.add_contact, name="add_contact"),
    path('admin-dash', views.admin_dash, name="admin_dash"),
    path('add-organization', views.add_organization, name="add_organization"),
    path('add-product', views.add_product, name="add_product"),
    path('add-entitlement', views.add_entitlement, name="add_entitlement"),
    path('get-contact-data', views.get_contact_data, name="get_contact_data"),
    path('get-org-data', views.get_org_data, name='get_org_data'),
    path('get-product-data', views.get_product_data, name='get_product_data'),
    path('get-entitlement-data', views.get_entitlement_data, name='get_entitlement_data'),

    path('delete-contact-selection/<str:query_string>/', views.delete_contact_selection, name='delete_contact_selection'),
    path('delete-org-selection/<str:query_string>/', views.delete_org_selection, name='delete_org_selection'),
    # path('delete-org-selection/<str:query_string>/redirect', views.delete_org_redirect, name='delete_org_redirect'),
    path('delete-product-selection/<str:query_string>/', views.delete_product_selection, name='delete_product_selection'),
    path('delete-entitlement-selection/<str:query_string>/', views.delete_entitlement_selection, name='delete_entitlement_selection'),



]