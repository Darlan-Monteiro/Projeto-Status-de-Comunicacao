from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def config_navegador():
    load_dotenv()
    caminho_user_chorme = os.getenv('caminho_user_chorme')
    site_dsp = os.getenv('site_dsp')
    s = Service('./msedgedriver.exe')
    dsp_automation = webdriver.EdgeOptions()
    dsp_automation.add_argument(caminho_user_chorme)
    driver = webdriver.Chrome(service=s, options=dsp_automation)
    driver.get(site_dsp)
    return driver

def web(sn_list):
    driver = config_navegador()
    pesquisa = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'input-field')))
    pesquisa.send_keys('12345678' + Keys.ENTER)
    time.sleep(0.2)

    dh_ultimo_ping_dict = {}  # Dicionário para armazenar SN e data/hora

    for sn in sn_list:  # Usando a lista de SNs passada como parâmetro
        x_barra_pesquisa = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'clear-search')))
        time.sleep(0.5)
        x_barra_pesquisa.click()

        busca = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'input-field')))
        time.sleep(0.5)
        busca.click()
        busca.send_keys(sn + Keys.ENTER)

        print('teste1')

        try:
            sn_element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="td-0-0"]/div/div/dsp-next-gen-ui-dft-asset-info/div/span/div/div[2]/div[1]'))
            )
            time.sleep(0.5)
            sn_element.click()
            print("Clicou em 'Device Status'")
        except TimeoutException:
            print(f"Erro ao tentar clicar no 'Device Status' para {sn}")
            continue  # Pula para o próximo SN
        
        # Abre o 'Device Status' e coleta a data e hora
        time.sleep(2)
        engrenagem = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="multiSizeDrawer"]/div[2]/dsp-next-gen-ui-dft-asset-drawer/div/div[1]/div[1]/div[1]/div[1]/div[2]/img')))
        time.sleep(2)
        engrenagem.click()
        
        time.sleep(2.5)
        elemento = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="device-status"]/div[2]/div[1]/div/div/div[3]/div[1]/span[2]')))
        
        # Adiciona ao dicionário: chave é o SN, valor é apenas a data
        data = elemento.text.split(' ')[0]  # Pega apenas a data, descartando a hora e o "GMT"
        dh_ultimo_ping_dict[sn] = data

        # Fecha a janela de 'Device Status'
        time.sleep(2)
        x_device_status = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="device-status"]/div[1]/div/div/cc-icon')))
        time.sleep(0.5)
        x_device_status.click()

        time.sleep(0.5)
        x_aba_engrenagem = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="multiSizeDrawer"]/div[2]/dsp-next-gen-ui-dft-asset-drawer/div/div[1]/div[2]/div[2]/cc-icon')))
        time.sleep(0.5)
        x_aba_engrenagem.click()

        print(dh_ultimo_ping_dict)

    return dh_ultimo_ping_dict
