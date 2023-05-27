from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "longitude",
                type=OpenApiTypes.FLOAT,
                description="Longitude of the point (ex. ?longitude=20.506235)",
            ),
            OpenApiParameter(
                "latitude",
                type=OpenApiTypes.FLOAT,
                description="Latitude of the point (ex. ?latitude=50.046235)",
            ),
        ]
    )
    @action(detail=False, methods=["GET"])
    def nearest_place(self, request):
        """
        Get nearest place to point.\n
        Endpoint must take longitude and latitude in parameters.\n
        Longitude and latitude must be float type
        """
        longitude = request.GET.get("longitude")
        latitude = request.GET.get("latitude")

        if longitude is None or latitude is None:
            return Response(
                {"error": "Missing required parameters: longitude, latitude"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            longitude = float(longitude)
            latitude = float(latitude)
        except ValueError:
            return Response(
                {
                    "error": "Invalid parameter value: longitude "
                             "and latitude must be valid float number"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        point = Point(longitude, latitude, srid=4326)

        nearest_place = (
            Place.objects.annotate(distance=Distance("geom", point))
            .order_by("distance")
            .first()
        )

        serializer = self.get_serializer(nearest_place)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Get all places in the database """
        return super().list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create place

        Name: string

        Description: string

        Geom: string, format: Point('longitude', 'latitude') - longitude and latitude must be float type
        """
        return super().create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Get place information by its id"""
        return super().retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a place by its id

        Name: string

        Description: string

        Geom: string, format: Point('longitude', 'latitude') - longitude and latitude must be float type
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial update of a place by its id

        Name: string

        Description: string

        Geom: string, format: Point('longitude', 'latitude') - longitude and latitude must be float type
        """
        return super().partial_update(self, request, *args, **kwargs)
