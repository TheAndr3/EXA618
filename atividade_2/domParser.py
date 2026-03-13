from xml.dom.minidom import parse
import time 
import csv

start_time = time.time()
arquivo = 'sanjuanDomParser.csv'

mapa = './sanjuan.osm'

SanJuanOSM = parse(mapa)

print("Starting DOM Parser...")
nodes = SanJuanOSM.getElementsByTagName("node")

with open(arquivo, mode='w', newline='') as file:
    colunas = ['Lat', 'Lon', 'Amenity', 'Name']
    writer = csv.writer(file)

    writer.writerow(colunas)

    for n in nodes:
        lat = n.getAttribute("lat")
        lon = n.getAttribute("lon")
    
        nome = ""
        amenity = ""

        subtags = n.getElementsByTagName("tag")

        for s in subtags:
            k = s.getAttribute("k")
            v = s.getAttribute("v")

            if k == "name":
                nome = v
            if k == "amenity":
                amenity = v
            
        if nome != "" and amenity != "":
            writer.writerow([lat, lon, amenity, nome])
                
end_time = time.time()
print(f"DOM Parser completed in {end_time - start_time} seconds.")

