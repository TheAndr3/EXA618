import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

arquivo = 'seeds.txt'

urls = []

def scrap():
        dados = []

        with open(arquivo, 'r') as f:
            for line in f:
                url = line.strip()
                urls.append(url)

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                titulo = soup.title.string if soup.title else url
                img = soup.find('img')
                img_url = "https://via.placeholder.com/150"  

                if img and img.get('src'):
                    img_url = urljoin(url, img['src'])
                
                dados.append({'titulo': titulo, 'url': url, 'img_url': img_url})
            except requests.RequestException as e:
                print(f"Erro ao acessar {url}: {e}")

        return dados

def gerar_html(dados):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<html><head><title>Resultados do Scraping</title></head><body>')
        f.write('<h1>Resultados do Scraping</h1>')
        f.write('<ul>')
        for item in dados:
            f.write(f'<li><a href="{item["url"]}">{item["titulo"]}</a><br><img src="{item["img_url"]}" alt="Imagem"></li>')
        f.write('</ul>')
        f.write('</body></html>')


if __name__ == "__main__":
    dados = scrap()
    gerar_html(dados)