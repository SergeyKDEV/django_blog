from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'

handler500 = 'core.views.internal_server_error'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/',
                    include(debug_toolbar.urls)),)
