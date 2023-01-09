from django.test import TestCase

from .models import Place


class TestPlaceModel(TestCase):
    def create_sample_place(self):
        return Place(
            code="sample_code",
            address="athens",
            location_lat=1.23,
            location_lon=2.34,
            name="sample_name",
            reward_checkin_points=1,
            tags=["sample_tag1", "sample_tag2"],
            type="office"
        )

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


class TestPlaceListAll(TestCase):
    pass
    # TODO Setup with 3 places
    # TODO Test all places are returned
    # TODO Test that searching works
    # TODO Test that ordering works
    # TODO Test that 200 is returned


class TestPlaceGetSpecific(TestCase):
    pass
    # TODO Setup with one place
    # TODO Test correct one is returned
    # TODO Test status code returned
    # TODO Test error when fetching with wrong uuid


class TestPlaceCreation(TestCase):
    pass
    # TODO Test proper creation
    # TODO Test status code and returned place
    # TODO Test invalid data


class TestPlaceModification(TestCase):
    pass
    # TODO Setup with one place
    # TODO Test uuid is not editable
    # TODO Test fields modified
    # TODO Test tags modified
    # TODO test non existing uuid


class TestPlaceDeletion(TestCase):
    pass
    # TODO Setup with one place
    # TODO Test deletion status code and body
    # TODO Tests non existence after deletion
    # TODO test non existing uuid
