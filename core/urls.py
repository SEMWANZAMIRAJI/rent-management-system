
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tenants.urls',)),
    path("contracts/", include("contracts.urls")),
    path("payments/", include("payments.urls")),
    path("notifications/", include("notifications.urls")),
    path('houses/', include('houses.urls', namespace='houses')),  


]
