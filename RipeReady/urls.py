from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Store app
    path("", include("store.urls", namespace="store")),

    # Cart app
    path("cart/", include("cart.urls", namespace="cart")),

    # Account app
    path("account/", include("account.urls", namespace="account")),

    # Django built-in authentication
    path("accounts/", include("django.contrib.auth.urls")),
    path("payment/", include("payment.urls", namespace="payment")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
