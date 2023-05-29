from django.contrib.gis.geos import GEOSGeometry, GEOSException
from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")

    def validate_geom(self, data):
        try:
            geom = GEOSGeometry(data)
        except (ValueError, TypeError) as e:
            raise serializers.ValidationError(f"Invalid data. Must be 'Point (20.50 50.20)'(example)")
        except GEOSException as e:
            raise serializers.ValidationError(str(e))

        if geom.geom_type != "Point":
            raise serializers.ValidationError(
                "Invalid point geometry. Must be Point type"
            )

        if abs(geom.x) > 180 or abs(geom.y) > 90:
            raise serializers.ValidationError(
                "Invalid coordinate range. "
                "Longitude must be in range -180 to 180, latitude in -90 to 90"
            )

        return data
