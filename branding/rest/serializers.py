from branding.models import HeroBrand, FeaturedBanner
from rest_framework import serializers


class HeroBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBrand
        fields = "__all__"


class FeaturedBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedBanner
        fields = "__all__"
