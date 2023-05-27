from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(detail=False, methods=["GET"])
    def nearest_place(self, request):
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
