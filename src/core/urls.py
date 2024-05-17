from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Trading Platform Administration'
admin.site.site_title = 'Trading Platform Admin'
admin.site.index_title = 'Welcome to Trading Platform Admin'

urlpatterns = [
    path("admin/", admin.site.urls),
]
