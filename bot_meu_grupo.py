from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


options = Options()
# options.set_headless = True
# options.add_argument('--disable-gpu')
# options.add_argument('--window-size=0,0')
options.add_argument(r'--user-data-dir=./User_Data')
driver = webdriver.Chrome(options=options)
url = 'https://web.whatsapp.com/'
driver.get(url)

print('Olá! O bot marcará todas as mensagens como lidas e fará o relatório para números desconhecidos')
grupo = str(input('Nome do grupo: '))

while True:
    while True:
        try:
            new = driver.find_element_by_class_name("OUeyt")
        except:
            pass
        else:
            print('Nova mensagem')
            break

    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, "pane-side")))

    sauce = driver.page_source
    soup = BeautifulSoup(sauce, 'html.parser')

    time.sleep(1)
    nova = soup.find('span', {'class': 'OUeyt'})
    time.sleep(1)
    new.click()
    time.sleep(3)
    marcar_como_lida = driver.find_element_by_xpath("//*[@id='app']/div/span[4]/div/ul/li[5]/div")
    time.sleep(1)
    marcar_como_lida.click()
    time.sleep(1)
    num = nova.find_previous('span', {'class': '_1wjpf _3NFp9 _3FXB1', 'dir': 'auto'}, title=True).text

    if '+' in num:
        hora = nova.find_previous('div', {'class': '_3Bxar'}, string=True).text
        msg = nova.find_previous('span', {'class': '_2_LEW'}).text
        numlink = num.replace('+', '').replace(' ', '').replace('-', '')
        print(num, hora, msg)

        time.sleep(2)
        caixa_de_pesquisa = driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]")
        caixa_de_pesquisa.clear()
        caixa_de_pesquisa.send_keys(grupo)
        time.sleep(3)
        caixa_de_pesquisa.send_keys(Keys.ARROW_DOWN)

        relatorio = f'*NOVO CONTATO*\n\n*Número*\n{num}\n\n*Mensagem*\n{msg}\n\n*Horário*\n{hora}\n\n*Link da conversa*\nhttps://wa.me/{numlink}'

        time.sleep(1)
        caixa_de_mensagem = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
        caixa_de_mensagem.clear()
        time.sleep(1)

        for letra in relatorio:
            if letra != '\n':
                caixa_de_mensagem.send_keys(letra)
            else:
                caixa_de_mensagem.send_keys(Keys.SHIFT + Keys.ENTER)
        caixa_de_mensagem.send_keys(Keys.ENTER)

    else:
        pass
