def formatted_coordinates(lat, long):
    return str(lat) + ", " + str(long)


class CompanyClass:

    def __init__(self, name, address, latitude=-1, longitude=-1):
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return ("Company Name: " + str(self.name) +
                "\nCompany Address: " + str(self.address) +
                "\nLatitude: " + str(self.latitude) + " Longitude: " + str(self.longitude))
