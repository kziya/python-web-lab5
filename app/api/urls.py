from django.urls import path

from .views import user_list_view, user_detail_view, food_detail_view, food_list_view, order_list_view

urlpatterns = [
    # User URLs
    path('user/', user_list_view, name='user_list'),
    path('user/<int:user_id>/', user_detail_view, name='user_detail'),

    # Food URLs
    path('food/', food_list_view, name='food_list'),
    path('food/<int:food_id>/', food_detail_view, name='food_detail'),

    # Order URLs
    path('order/', order_list_view, name='order_list'),
]
