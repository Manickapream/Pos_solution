from rest_framework import serializers
from .models import Product, Inquiry


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'image_url', 'description', 'status', 'created_at']
        extra_kwargs = {'image': {'required': False}}

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'product_name', 'price', 'name', 'email', 'mobile', 'message', 'created_at']
