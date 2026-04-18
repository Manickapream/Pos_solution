from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Product, Inquiry, AuthAdmin
from .serializers import ProductSerializer, InquirySerializer


# ─────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────
class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {'success': False, 'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate against auth_admin table
        try:
            admin = AuthAdmin.objects.get(email=email, is_active=True)
        except AuthAdmin.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if admin.check_password(password):
            return Response({
                'success': True,
                'admin_id': admin.id,
                'name': admin.name,
                'email': admin.email,
                'role': 'Admin',
                'message': 'Login successful'
            })

        return Response(
            {'success': False, 'message': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


# ─────────────────────────────────────────
#  PRODUCTS
# ─────────────────────────────────────────
class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.filter(status='Active').order_by('-created_at')
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Only Admin (superuser) can create
        role = request.headers.get('X-User-Role') # Simple role check for now, can be improved with JWT or Session
        if not request.user.is_superuser and role != 'Admin':
             return Response({'error': 'Only Admins can create products'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAllView(APIView):
    """Admin view – returns ALL products regardless of status."""
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_superuser and request.headers.get('X-User-Role') != 'Admin':
            return Response({'error': 'Only Admins can edit products'}, status=status.HTTP_403_FORBIDDEN)
            
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data,
                                       partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_superuser and request.headers.get('X-User-Role') != 'Admin':
            return Response({'error': 'Only Admins can delete products'}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'success': True, 'message': 'Product deleted'})


# ─────────────────────────────────────────
#  INQUIRIES
# ─────────────────────────────────────────
class InquiryListCreateView(APIView):
    def get(self, request):
        inquiries = Inquiry.objects.all().order_by('-created_at')
        serializer = InquirySerializer(inquiries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Inquiry submitted successfully!'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InquiryDeleteView(APIView):
    def delete(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        inquiry.delete()
        return Response({'success': True, 'message': 'Inquiry deleted'})


# ─────────────────────────────────────────
#  DASHBOARD STATS
# ─────────────────────────────────────────
class DashboardStatsView(APIView):
    def get(self, request):
        return Response({
            'total_products': Product.objects.filter(status='Active').count(),
            'total_inquiries': Inquiry.objects.count(),
            'total_all_products': Product.objects.count(),
        })
