import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Place

PLACE_API_URL = '/api/place'


class TestPlaceModel(TestCase):
    def create_sample_place(self):
        p = Place(
            code="sample_code",
            address="athens",
            location_lat=1.23,
            location_lon=2.34,
            name="sample_name",
            reward_checkin_points=1,
            type="office"
        )
        p.tags.add("sample_tag_1", "sample_tag_2")
        return p

    def test_place_uuid_auto_generated(self):
        p = self.create_sample_place()
        p.save()
        assert p.uuid

    def test_place_address_nullable(self):
        p = self.create_sample_place()
        p.address = None
        p.save()
        assert not p.address

    def test_place_name_nullable(self):
        p = self.create_sample_place()
        p.name = None
        p.save()
        assert not p.name

    def test_place_tags_nullable(self):
        p = self.create_sample_place()
        p.tags = None
        p.save()
        assert not p.tags


class TestPlaceGetAll(TestCase):
    sample_codes = ["A", "B", "C"]
    sample_addresses = ["athens", "patra", "naxos"]

    @classmethod
    def store_sample_place(cls, code, address):
        p = Place(
            code=code,
            address=address,
            location_lat=1.23,
            location_lon=2.34,
            name="sample_name",
            reward_checkin_points=1,
            type="office"
        )
        p.tags.add("sample_tag_1", "sample_tag_2")
        p.save()

    @classmethod
    def setUpTestData(cls):
        for code, address in zip(cls.sample_codes, cls.sample_addresses):
            cls.store_sample_place(code, address)

    def test_get_all_places(self):
        response = self.client.get(PLACE_API_URL)
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_body), len(self.sample_codes))

    def test_get_all_places_search(self):
        response = self.client.get(PLACE_API_URL+f"?search={self.sample_addresses[0]}")
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_body), 1)
        self.assertEqual(res_body[0]['address'], self.sample_addresses[0])

    def test_get_all_places_reverse_order_on_code(self):
        response = self.client.get(PLACE_API_URL+f"?ordering=-code")
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_body), 3)

        rev_sample_addresses = self.sample_addresses.copy()
        rev_sample_addresses.reverse()
        for address, item in zip(rev_sample_addresses, res_body):
            self.assertEqual(item['address'], address)


class TestPlaceGetSpecific(TestCase):
    def create_place(self):
        p = Place(
            code="sample_code",
            address="sample_address",
            location_lat=1.23,
            location_lon=2.34,
            name="sample_name",
            reward_checkin_points=1,
            type="office"
        )
        p.tags.add("sample_tag_1", "sample_tag_2")
        p.save()
        return p

    def test_get_specific_place(self):
        p = self.create_place()
        response = self.client.get(PLACE_API_URL+f"/{p.uuid}/")
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(p.uuid), res_body['uuid'])
        self.assertEqual(p.code, res_body['code'])
        self.assertEqual(p.address, res_body['address'])
        self.assertEqual(p.location_lat, res_body['location']['lat'])
        self.assertEqual(p.location_lon, res_body['location']['lon'])
        self.assertEqual(p.name, res_body['name'])
        self.assertEqual(p.reward_checkin_points, res_body['reward_checkin_points'])
        self.assertEqual(len(p.tags.all()), len(res_body['tags']))
        self.assertEqual(p.type, res_body['type'])

    def test_get_specific_place_non_existing_uuid(self):
        response = self.client.get(PLACE_API_URL+f"/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPlacePost(TestCase):
    def create_place_data(self):
        return {
            "address": "Voutadon 29-23, Athina 118 54",
            "code": "000000A",
            "location": {
                "lat": 37.978693,
                "lon": 23.712884
            },
            "name": "HQ",
            "reward_checkin_points": 1,
            "tags": [
                "innovation_center",
                "popular",
                "favorite",
            ],
            "type": "office"
        }

    def test_post_place(self):
        request_data = self.create_place_data()
        response = self.client.post(PLACE_API_URL, request_data, content_type='application/json')
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("uuid", res_body.keys())
        self.assertEqual(Place.objects.count(), 1)

        # Remove uuid, sort tags and compare the 2 dicts
        del res_body["uuid"]
        res_body["tags"].sort()
        request_data["tags"].sort()
        self.assertDictEqual(request_data, res_body)

    def test_post_place_bad_request(self):
        request_data = self.create_place_data()
        request_data["code"] = "very loooooooooooooong code"
        response = self.client.post(PLACE_API_URL, request_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestPlacePut(TestCase):
    @classmethod
    def get_sample_place_dict(cls):
        return {
            "address": "Voutadon 29-23, Athina 118 54",
            "code": "000000A",
            "location": {
                "lat": 37.978693,
                "lon": 23.712884
            },
            "name": "HQ",
            "reward_checkin_points": 1,
            "type": "office"
        }

    @classmethod
    def setUpTestData(cls):
        place = cls.get_sample_place_dict()
        p = Place(
            code=place["code"],
            address=place["address"],
            location_lat=place["location"]["lat"],
            location_lon=place["location"]["lon"],
            name=place["name"],
            reward_checkin_points=place["reward_checkin_points"],
            type=place["type"]
        )
        p.save()

    def test_put_place(self):
        place = Place.objects.all()[0]

        request_data = self.get_sample_place_dict()
        request_data["name"] = "new_name"

        response = self.client.put(PLACE_API_URL+f"/{place.uuid}/", request_data, content_type='application/json')
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res_body["uuid"], str(place.uuid))
        self.assertEqual(res_body["name"], request_data["name"])

        # Fetch place from database again
        place = Place.objects.get(uuid=place.uuid)
        self.assertEqual(place.name, request_data["name"])

    def test_put_place_uuid_non_editable(self):
        place = Place.objects.all()[0]

        request_data = self.get_sample_place_dict()
        request_data["uuid"] = uuid.uuid4()

        response = self.client.put(PLACE_API_URL+f"/{place.uuid}/", request_data, content_type='application/json')
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res_body["uuid"], str(request_data["uuid"]))

    def test_put_place_tags_modified(self):
        new_tag = "new_tag"
        place = Place.objects.all()[0]

        request_data = self.get_sample_place_dict()
        request_data["tags"] = [new_tag]

        response = self.client.put(PLACE_API_URL+f"/{place.uuid}/", request_data, content_type='application/json')
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(new_tag, res_body["tags"])

    def test_put_place_non_existing_uuid(self):
        response = self.client.put(PLACE_API_URL+f"/{uuid.uuid4()}/", {}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPlaceDelete(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Place(
            code="sample_code",
            address="sample_address",
            location_lat=1.23,
            location_lon=2.34,
            name="sample_name",
            reward_checkin_points=1,
            type="office"
        )
        p.save()

    def test_delete_place(self):
        place = Place.objects.all()[0]

        response = self.client.delete(PLACE_API_URL+f"/{place.uuid}/")
        res_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res_body["uuid"], str(place.uuid))
        self.assertEqual(len(Place.objects.all()), 0)

    def test_delete_place_non_existing_uuid(self):
        response = self.client.delete(PLACE_API_URL+f"/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
