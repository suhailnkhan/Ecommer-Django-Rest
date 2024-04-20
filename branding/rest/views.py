from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from branding.rest.serializers import HeroBrandSerializer, FeaturedBannerSerializer
from branding.models import HeroBrand, FeaturedBanner
from rest_framework.status import *

from blinkbuy_web.utils import get_full_image_url


class CreateListHeroBrand(ListCreateAPIView):
    serializer_class = HeroBrandSerializer
    queryset = HeroBrand.objects.all()

    def get(self, request, *args, **kwargs):
        data = []
        for q in self.get_queryset():
            tempDict = {
                "id": q.id,
                "title": q.title,
                'slug': q.title,
                "link": q.link,
                "image": {
                    "mobile": {
                        "url": get_full_image_url(request, q.image),
                        "width": 690,
                        "height": 480,
                    },
                    "desktop": {
                        "url": get_full_image_url(request, q.image),
                        "width": 1800,
                        "height": 800,
                    },
                },
            }
            data.append(tempDict)
        return Response({"data": data})


class CreateListFeaturedBanner(ListCreateAPIView):
    serializer_class = FeaturedBannerSerializer
    queryset = FeaturedBanner.objects.all()

    def get(self, request, *args, **kwargs):
        data = []
        for q in self.queryset.all():
            tempDict = {
                "id": q.id,
                "title": q.title,
                "link": q.link,
                "sub_title": q.sub_title,
                "image": get_full_image_url(request, q.image),
            }
        data.append(tempDict)

        return Response({"data": data})
