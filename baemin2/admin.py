from django.contrib import admin
from .models import *

class ItemInline(admin.StackedInline):
	model = Item
	extra = 2

class MenuCategoryInline(admin.TabularInline):
	model = MenuCategory
	extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']
	inlines = [MenuCategoryInline, ItemInline]

@admin.register(ShopDesc)
class ShopDescAdmin(admin.ModelAdmin):
	pass

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
	inlines = [ItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['id', 'shop', 'author']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	pass
