from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from .models import User, Food, Order

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email',)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'food')
    search_fields = ('user__email', 'food__name')
