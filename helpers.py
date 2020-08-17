import requests
from bs4 import BeautifulSoup
import datetime
import re 
import numpy as np 


def scrapingportal_inmobiliario(region,pages):
     
     #Crear listas vacias para almacenar variables
    attributes = []
    address = []
    m2 = []
    rooms = []
    toilets = []
    prices = []
    urls = []

    print("Running Web Scraping Portal Inmobiliario...")
    #Bucle para avanzar por las paginas de resultados de portal inmobiliario
    for i in range(1,pages*50,50):
        url = 'https://www.portalinmobiliario.com/arriendo/departamento/'+region+'/_Desde_'+ str(i)

        #Obtener el codigo HTML de cada pagina
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        containers = soup.find_all('div',class_='item__info-container')

        print(f"Page Fully Loaded!")

        #Bucle para  acceder a items con información de arriendo por cada pagina

        for container in containers:
            #Agregar información en listas creadas más arriba
            try:
                prices.append(container.find('span',class_='price__fraction').text)
                attributes.append(container.find('div',class_='item__attrs').text)
                address.append(container.find('span',class_='main-title nowrap').text)
                urls.append(container.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'])
            except AttributeError:
                pass

        print(f"prices: +{len(prices)} + attributes: +{len(attributes)}  address: +{len(address)}")

    print('Webscraping Finished\n')

    #Separar valores de atributos en  nuevas listas, debido a que por la estructura de la pagina web 
    estos valores se guardan en la misma categoria.

    for attribute in attributes:
        temp_value  = attribute.split('|')
        try:
            m2.append(temp_value[0])

            rooms.append(temp_value[1])
            if len(rooms) != len(m2):
                rooms.append(np.nan)
        
            toilets.append(temp_value[2])
            if len(toilets) != len(rooms):
                toilets.append(np.nan)
        except  IndexError:
            pass

    return prices,address,m2,rooms,toilets,urls


 
        

  








