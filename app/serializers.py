from rest_framework import serializers
from . models import *


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['key', 'value']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    specifications = SpecificationSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)