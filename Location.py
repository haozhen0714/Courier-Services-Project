import gmplot
API_KEY = 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'

gmapOne=gmplot.GoogleMapPlotter(3.112585695236, 101.6397000538541, 10,API_KEY=API_KEY)
gmapOne.apikey= 'AIzaSyDKQY-dAMpv32uiWSREDRH83FZRcNUhSmw'
gmapOne.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
gmapOne.marker(3.0319924887507144,101.37344116244806,color='blue',title='Port Klang')
gmapOne.marker(3.112924170027219,101.63982650389863,color='red',title='Petaling Jaya')
gmapOne.marker(3.265154613796736,101.68024844550233,color='yellow',title='Batu Caves')
gmapOne.marker(2.9441205329488325,101.7901521759029,color='black',title='Kajang')
gmapOne.marker(3.2127230893650065,101.57467295692778,color='orange',title='Sungai Buloh')

# lat=[3.0319924887507144,3.112924170027219,3.265154613796736,2.9441205329488325,3.2127230893650065]
# lang=[101.37344116244806,101.63982650389863,101.68024844550233,101.7901521759029,101.57467295692778]

# gmapOne.scatter(lat,lang,'#ff000',size=100,marker=True)
# gmapOne.plot(lat,lang,'blue',edge_width=2.5)
gmapOne.draw("map.html")


