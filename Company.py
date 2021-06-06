def formatted_coordinates(lat, long):
    return str(lat) + ", " + str(long)


class CompanyClass:

    def __init__(self, name, address, latitude=-1, longitude=-1, url_list=None, positive=0, negative=0,
                 positive_percentage=0):
        if url_list is None:
            url_list = []
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.url_list = url_list
        self.positive = positive
        self.negative = negative
        self.positive_percentage = positive_percentage

    def calc_positive_percentage(self):
        self.positive_percentage = (self.positive / (self.positive + self.negative)) * 100

    def __str__(self):
        return ("Company Name: " + str(self.name) +
                "\nCompany Address: " + str(self.address) +
                "\nLatitude: " + str(self.latitude) + " Longitude: " + str(self.longitude) +
                "\nPositive Word: " + str(self.positive) +
                "\nNegative Word: " + str(self.negative) +
                "\nPositive Percentage: " + str(self.positive_percentage))


