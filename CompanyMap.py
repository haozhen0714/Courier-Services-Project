import gmplot

from Company import CompanyClass

API_KEY = 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'


def read_company_full_details():
    company_file = open("Company_Full_Details.txt", "r")
    company_all_list = company_file.readlines()
    company_object_list = []
    c = []
    while len(company_all_list) != 0:
        for i in range(4):
            c.append(company_all_list.pop(0).replace('\n', ''))
        if len(company_all_list) != 0:
            company_all_list.pop(0)
        company_object_list.append(CompanyClass(c[0], c[1], c[2], c[3]))
        c = []
    company_file.close()
    return company_object_list


def draw_company_map():
    gmapOne = gmplot.GoogleMapPlotter(3.112585695236, 101.6397000538541, 10, API_KEY=API_KEY)
    gmapOne.apikey = API_KEY
    gmapOne.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    color_list = ['blue', 'red', 'yellow', 'black', 'orange']
    company_list = read_company_full_details()
    for i in range(len(company_list)):
        gmapOne.marker(float(company_list[i].latitude), float(company_list[i].longitude),
                       color=color_list[i], title=company_list[i].name)

    # lat=[3.0319924887507144,3.112924170027219,3.265154613796736,2.9441205329488325,3.2127230893650065]
    # lang=[101.37344116244806,101.63982650389863,101.68024844550233,101.7901521759029,101.57467295692778]

    # gmapOne.scatter(lat,lang,'#ff000',size=100,marker=True)
    # gmapOne.plot(lat,lang,'blue',edge_width=2.5)
    gmapOne.draw("Company Map.html")
