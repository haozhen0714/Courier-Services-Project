import DistanceMatrixAPI


def formatted_coordinates(lat, long):
    return str(lat) + ", " + str(long)


class CustomerClass:

    def __init__(self, customer_name, ori_name, ori_lat, ori_long, des_name, des_lat, des_long, direct_distance=""):
        self.customer_name = customer_name
        self.ori_name = ori_name
        self.ori_lat = ori_lat
        self.ori_long = ori_long
        self.des_name = des_name
        self.des_lat = des_lat
        self.des_long = des_long
        self.direct_distance = direct_distance
        self.calc_direct_distance()

    def calc_direct_distance(self):
        self.direct_distance = DistanceMatrixAPI.calc_distance_between_2_point(
            formatted_coordinates(self.ori_lat, self.ori_long),
            formatted_coordinates(self.des_lat, self.des_long)
        )

    def __str__(self):
        return (str(self.customer_name) +
                "\nOri_Lat: " + self.ori_lat + " Ori_Long: " + self.ori_long +
                "\nDes_Lat: " + self.des_lat + " Des_Long: " + self.des_long +
                "\nHaving Distance of: " + self.direct_distance)
