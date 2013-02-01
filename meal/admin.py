from django.contrib import admin
from meal.models import Meal
from meal.models import Ingredient

class MealAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Meal, MealAdmin)
