from django.test import TestCase

from geo_data.serializers import PlaceSerializer


class PlaceSerializerTests(TestCase):
    def test_valid_data(self):
        point = {
            "name": "Point",
            "description": "Point description",
            "geom": "POINT (50.2050 10.500)"
        }

        serializer = PlaceSerializer(data=point)
        self.assertTrue(serializer.is_valid())

    def test_invalid_geom_data(self):
        point = {
            "name": "Point",
            "description": "Point description",
            "geom": "Invalid data"
        }

        serializer = PlaceSerializer(data=point)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Invalid data. Must be 'Point (20.50 50.20)'(example)",
            serializer.errors["geom"]
        )

    def test_invalid_geom_type(self):
        point = {
            "name": "Point",
            "description": "Point description",
            "geom": "LINESTRING (0 0, 1 1)"
        }

        serializer = PlaceSerializer(data=point)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Invalid point geometry. Must be Point type",
            serializer.errors["geom"]
        )

    def test_invalid_geom_lon_lat_separate_by_comma(self):
        point = {
            "name": "Point",
            "description": "Point description",
            "geom": "POINT (50.2050, 10.500)"
        }

        serializer = PlaceSerializer(data=point)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'Error encountered checking Geometry returned from GEOS C function "GEOSWKTReader_read_r".',
            serializer.errors["geom"]
        )

    def test_invalid_geom_value_out_of_range(self):
        point = {
            "name": "Point",
            "description": "Point description",
            "geom": "POINT (190.205 -100.500)"
        }

        serializer = PlaceSerializer(data=point)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Invalid coordinate range. "
            "Longitude must be in range -180 to 180, latitude in -90 to 90",
            serializer.errors["geom"]
        )
