from django.contrib import admin

# Register your models here.
from sales.models import Post, Category, Person

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Person)
