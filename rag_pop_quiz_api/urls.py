from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    
    path(r'', admin.site.urls),
]
admin.site.site_header = "habahaba Admin"
admin.site.site_title = "habahaba Admin Portal"
admin.site.index_title = "habahaba Administrator portal"
