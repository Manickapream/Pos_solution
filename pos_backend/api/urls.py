from django.urls import path
from .views import (
    AdminLoginView,
    ProductListCreateView,
    ProductAllView,
    ProductDetailView,
    InquiryListCreateView,
    InquiryDeleteView,
    DashboardStatsView,
)

urlpatterns = [
    # Auth
    path('auth/login/', AdminLoginView.as_view(), name='admin-login'),

    # Products – public listing (Active only)
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    # Products – admin (all)
    path('products/all/', ProductAllView.as_view(), name='product-all'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Inquiries
    path('inquiries/', InquiryListCreateView.as_view(), name='inquiry-list-create'),
    path('inquiries/<int:pk>/', InquiryDeleteView.as_view(), name='inquiry-delete'),

    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
