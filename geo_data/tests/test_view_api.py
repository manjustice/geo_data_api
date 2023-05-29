from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from geo_data.models import Place
from geo_data.serializers import PlaceSerializer


PLACE_LIST_URL = reverse("geo:place-list")


def place_detail_url(place_id: int) -> str:
    return reverse("geo:place-detail", args=[place_id])


class PlaceViewTests(TestCase):
    def setUp(self):
        self.first_place = Place.objects.create(
            name="First place",
            description="Description of the first place",
            geom="POINT (8.00505050 45.0000000)"
        )
        self.second_place = Place.objects.create(
            name="Second place",
            description="Description of the second place",
            geom="POINT (10.0000000 45.0000000)"
        )

    def check_for_equality(self, payload, place):
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(place, key))

    def test_get_list_of_places(self):
        res = self.client.get(PLACE_LIST_URL)

        places = Place.objects.all()

        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_place(self):
        res = self.client.get(place_detail_url(self.first_place.id))

        serializer = PlaceSerializer(self.first_place)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_place(self):
        payload = {
            "name": "New place",
            "description": "Description of the new place",
            "geom": "SRID=4326;POINT (15.0000000 40.0000000)",
        }
        res = self.client.post(PLACE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        place = Place.objects.get(id=res.data["id"])

        self.check_for_equality(payload, place)

    def test_update_place(self):
        payload = {
            "name": "Updated First Place",
            "description": "Updated description of the place",
            "geom": "SRID=4326;POINT (8.0000000 40.0000000)",
        }
        res = self.client.put(
            place_detail_url(self.first_place.id),
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        place = Place.objects.get(id=self.first_place.id)

        self.check_for_equality(payload, place)

    def test_delete_place(self):
        res = self.client.delete(place_detail_url(self.first_place.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_nearest_place(self):
        params = {"longitude": 9.00, "latitude": 45.00}
        res = self.client.get(reverse("geo:place-nearest-place"), params)

        serializer = PlaceSerializer(self.first_place)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_nearest_place_if_not_parameters(self):
        res = self.client.get(reverse("geo:place-nearest-place"))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data,
            {"error": "Missing required parameters: longitude, latitude"}
        )

    def test_nearest_place_if_one_parameter_is_missing(self):
        params = {"longitude": 9.00}
        res = self.client.get(reverse("geo:place-nearest-place"), params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data,
            {"error": "Missing required parameters: longitude, latitude"}
        )

    def test_nearest_place_if_parameter_is_not_float(self):
        params = {"longitude": 9.00, "latitude": "latitude"}
        res = self.client.get(reverse("geo:place-nearest-place"), params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data,
            {
                "error": "Invalid parameter value: longitude "
                         "and latitude must be valid float number"
            }
        )
