import requests


class LicensePlateValidator:
    API_URL = "http://localhost:5000"

    def validate_plate(self, plate_number):
        response = requests.post(self.API_URL, json={"plate_number": plate_number})
        if response.status_code == 200:
            return response.json().get("allowed", False)
        else:
            response.raise_for_status()


licence_plate_validator = LicensePlateValidator()
print(licence_plate_validator.validate_plate("ABC123"))