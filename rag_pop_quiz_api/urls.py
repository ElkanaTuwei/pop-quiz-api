from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    
    path(r'', admin.site.urls),
]
admin.site.site_header = "Quiz Admin"
admin.site.site_title = "Quiz Admin Portal"
admin.site.index_title = "Quiz Administrator portal"
