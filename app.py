import json
from flask import Flask, jsonify
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from crochet import setup, wait_for

from scraping_suite.scrapy_project.spiders.aceite_oliva_spider import AceiteOlivaSpider
from scraping_suite.scrapy_project.spiders.calamar_spider import CalamarSpider
from scraping_suite.scrapy_project.spiders.camaron_spider import CamaronSpider

# Configurar Crochet para manejar el reactor
setup()

# Configurar el logging de Scrapy
configure_logging()

# Crear la aplicación Flask
app = Flask(__name__)

# Correr los spiders usando Crochet para manejar el reactor dentro de Flask
runner = CrawlerRunner()

# Lista para almacenar los items scrapeados
scraped_items = []

# Procesar los items scrapeados
class ItemCollectorPipeline:
    def process_item(self, item, spider):
        # Guardar los items scrapeados
        scraped_items.append(dict(item))
        return item

# Inyectar el pipeline en Scrapy
runner.settings.set('ITEM_PIPELINES', {'__main__.ItemCollectorPipeline': 1})

# Decorador para que el reactor corra de manera segura dentro de Flask
@wait_for(timeout=60.0)
@defer.inlineCallbacks
def run_spiders():
    global scraped_items
    scraped_items = []  # Limpiar los resultados anteriores

    # Ejecutar los spiders secuencialmente
    yield runner.crawl(AceiteOlivaSpider)
    yield runner.crawl(CalamarSpider)
    yield runner.crawl(CamaronSpider)

    # Retornar los items scrapeados
    defer.returnValue(scraped_items)

# Ruta de la API para ejecutar los spiders
@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        # Ejecutamos los spiders y obtenemos los resultados
        scraped_data = run_spiders()

        # Preparamos la respuesta JSON con los datos extraídos
        body = {
            "message": "Scraping completed successfully!",
            "data": scraped_data  # Aquí se incluirán los datos scrapeados
        }

        return jsonify(body), 200

    except Exception as e:
        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500

# Iniciar la aplicación Flask en el puerto 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

