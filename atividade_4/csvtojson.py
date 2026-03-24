import csv
import json

geojson = {
    "type": "FeatureCollection",
    "features": []
}

with open('SanJuanDOMParser.csv', mode='r', newline='', encoding='latin-1') as file:
    csv_reader = csv.DictReader(file)
    
    for i, row in enumerate(csv_reader):

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinantes" : [
                    float(row['Lon']),
                    float(row['Lat'])
                ]
            },
            "properties" : {
                "nome" : row['Name'],
                "tipo" : row['Amenity']
            },
            "id" : i
        }

        geojson["features"].append(feature)

with open('geo.geojson', 'w') as f:
    json.dump(geojson, f, ensure_ascii=True, indent=4)


