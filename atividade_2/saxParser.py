import xml.sax
import csv
import time

arquivo_saida = "SanJuanSAX_Filtered.csv"
mapa = './sanjuan.osm'
start_time = time.time()

class Listener(xml.sax.ContentHandler):
    def __init__(self, writer):
        self.writer = writer
        self.currentNode = {}
        self.has_name = False
        self.has_amenity = False

    def startElement(self, tag, attributes):
        if tag == "node":    
            # Reiniciamos os dados e os sinalizadores para cada novo nó
            self.currentNode = {
                "Lat": attributes.get("lat"),
                "Lon": attributes.get("lon"),
                "Amenity": "",
                "Name": ""
            }
            self.has_name = False
            self.has_amenity = False

        elif tag == "tag" and self.currentNode:
            k = attributes.get("k")
            v = attributes.get("v")

            if k == "name" and v:
                self.currentNode["Name"] = v
                self.has_name = True
            elif k == "amenity" and v:
                self.currentNode["Amenity"] = v
                self.has_amenity = True

    def endElement(self, tag):
        # Só gravamos se encontrar AMBOS durante a leitura das sub-tags
        if tag == "node":
            if self.has_name and self.has_amenity:
                self.writer.writerow([
                    self.currentNode["Lat"],
                    self.currentNode["Lon"],
                    self.currentNode["Amenity"],
                    self.currentNode["Name"]
                ])
            # Limpamos para garantir que dados de um nó não vazem para o próximo
            self.currentNode = {}

# --- Execução do Parser ---

with open(arquivo_saida, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Lat', 'Lon', 'Amenity', 'Name'])

    parser = xml.sax.make_parser()
    handler = Listener(writer)
    parser.setContentHandler(handler)

    print(f"Buscando locais com Nome E Amenity em {mapa}...")
    parser.parse(mapa)

end_time = time.time()
print("-" * 30)
print(f"Processamento concluído em {end_time - start_time:.4f} segundos.")
print(f"Os resultados foram salvos em: {arquivo_saida}")