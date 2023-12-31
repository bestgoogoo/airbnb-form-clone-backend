from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):
    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity Name"
    DESC = "Amenity Description"
    NEW_NAME = "New Amenity Name"
    NEW_DESC = "New Amenity Description"
    MAX_LENGTH_NAME = "N" * 151
    MAX_LENGTH_DESC = "D" * 151

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "GET Response Status Code isn`t 200.",
        )
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)

    def test_create_amenity(self):
        # Check for POST amenity
        response = self.client.post(
            self.URL,
            data={"name": self.NEW_NAME, "description": self.NEW_DESC},
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "POST Response Status Code isn`t 200.",
        )
        self.assertEqual(data["name"], self.NEW_NAME)
        self.assertEqual(data["description"], self.NEW_DESC)

        # Check for required "key" of amenity
        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

        # Check for "value" of amenity is max_length=150
        response = self.client.post(
            self.URL,
            data={"name": self.MAX_LENGTH_NAME, "description": self.MAX_LENGTH_DESC},
        )

        self.assertEqual(response.status_code, 400)


class TestAmenity(APITestCase):
    NAME = "Amenity Name"
    DESC = "Amenity Description"
    UPDATED_NAME = "Updated_amenity_name"
    UPDATED_DESC = "Updated_amenity_description"
    MAX_LENGTH_NAME = "N" * 151
    MAX_LENGTH_DESC = "D" * 151

    URL = "/api/v1/rooms/amenities/1"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get(f"{self.URL}2")

        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200)

    def test_put_amenity(self):
        # Check for PUT amenity
        response = self.client.put(
            self.URL,
            data={
                "name": self.UPDATED_NAME,
                "description": self.UPDATED_DESC,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], self.UPDATED_NAME)
        self.assertEqual(data["description"], self.UPDATED_DESC)

        # Check for required "key" of amenity is not necessary
        # Check for "value" of amenity is max_length=150
        response = self.client.put(
            self.URL,
            data={"name": self.MAX_LENGTH_NAME, "description": self.MAX_LENGTH_DESC},
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_amenity(self):
        response = self.client.delete(self.URL)

        self.assertEqual(response.status_code, 204)


class TestRoomsPermission(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        # self.user를 사용하므로 'class TestRooms()'안에 'def setUp()'밖에 user가 있는 것과 같이 함.
        self.user = user

    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)
        print(f"로그인 전: {response.json()}")

        # 강제로 로그인 시킴.
        self.client.force_login(self.user)

        # 여기는 로그인 됐다는 것을 확인하기 위한 코드이므로 없어도 됨.
        response = self.client.post("/api/v1/rooms/")
        print(f"로그인 후: {response.json()}")
