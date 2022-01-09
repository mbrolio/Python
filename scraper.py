import requests
from platform import release
from bs4 import BeautifulSoup
import cv2
from time import sleep
import numpy as np
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
import pandas as pd

#dados_revistas = []

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,640)
cap.set(4,480)

def get_url(pesquisa_cod):   
    template = 'https://www.amazon.com.br/s?k={}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss'
    pesquisa_cod = pesquisa_cod.replace(' ', '+')
    return template.format(pesquisa_cod)

while True:
    ret, video = cap.read()

    
    for barcode in decode(video):
#       print(barcode.data)
        myData = barcode.data.decode('utf-8')
#       elemento = navegador.find_element_by_id('twotabsearchtextbox')
#       elemento.send_keys(myData)
#       elemento.submit()

        dados_revistas = []

        url = get_url(myData)
        navegador = webdriver.Chrome()
        navegador.get(url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')    
        
        sleep(1)

        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'lxml')
                        
        revista = site.find('div', attrs={'class': 'a-section a-spacing-medium'})
               
        #revista_nome = revista.findAll('span', attrs={'class' : 'a-size-medium a-color-base a-text-normal'})
        revista_nome = revista.h2.span.text
        print ('Código de Barra: ', myData)
        print ('Nome da Revista: ', revista_nome)

        revista_imagem = site.find('img', attrs={'class' : 's-image'}).get('src')
        print ('Capa: ', revista_imagem)

        dados_revistas.append([myData, revista_imagem, revista_nome])
        #dados = pd.DataFrame(dados_revistas, columns=['Código de Barra', 'Capa', 'Nome da Revista'])
        dados = pd.DataFrame(dados_revistas)
        #sorted_dados = dados.sort_values(by=[revista_nome], ascending=False)
        dados.to_csv('revistas.csv', mode='a', sep = ';', encoding='utf-8', index=False)
        #sorted_dados.to_csv('revistas_sorted.csv', sep = ';', encoding = 'utf-8' , index=False)


        elemento = navegador.find_element_by_id('twotabsearchtextbox')
        elemento.clear()
          
    cv2.imshow('frame', video)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
