import unittest

from rest_api.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_list_activities(self):
        response = self.app.get('/activity/')
        self.assertEqual(response.status_code, 200)

    def test_create_activity(self):
        response = self.app.post('/activity/', json={
            "car_id": 1,
            "spot_id": 1,
            "entrance_timestamp": "2023-01-01T00:00:00Z",
            "leave_timestamp": "2023-01-01T01:00:00Z"
        })
        self.assertEqual(response.status_code, 201)

    def test_list_cars(self):
        response = self.app.get('/cars/')
        self.assertEqual(response.status_code, 200)

    def test_create_car(self):
        response = self.app.post('/cars/', json={"registration_number": "ABC123"})
        self.assertEqual(response.status_code, 201)

    def test_list_available_spots(self):
        response = self.app.get('/parking/available')
        self.assertEqual(response.status_code, 200)

    def test_create_parking_spot(self):
        response = self.app.post('/parking/', json={"spot_number": 1})
        self.assertEqual(response.status_code, 201)

    def test_update_parking_status(self):
        response = self.app.patch('/parking/1/update', json={"car_id": 1})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
