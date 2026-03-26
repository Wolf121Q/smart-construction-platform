from rest_framework import serializers
from vendor_company.models import BusinessType, VendorType, VendorCompany

class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = '__all__'

class VendorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorType
        fields = '__all__'

class VendorCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorCompany
        fields = '__all__'


