from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import io
from datetime import datetime
import re

# Abrindo o browser, cookies pra não ter que ler o QR code sempre
options = Options()
options.add_argument(r'--user-data-dir=./User_Data')
driver = webdriver.Chrome(options=options)
url = 'https://web.whatsapp.com/'
driver.get(url)
act = ActionChains(driver)

input("Pressione qualquer tecla depois de ler o QR code ou da página carregar")

# Classes e XPATH. Caso haja algum problema, provavelmente o wpp atualizou. Basta mudá-las nestas variáveis
c_fixada = '_1EFSv'
c_itenscv = '_2hqOq'
c_recebidas = 'message-in'
c_enviadas = 'message-out'
c_bolha = '_31gEB'
c_contato = '_210SC'
c_cabecalho = '_1iFv8'
c_numaberto = '_3ko75 _5h6Y_ _3Whw5'
x_caixamsg = "//*[@id='main']/footer/div[1]/div[2]/div"
x_caixapesq = "//*[@id='side']/div[1]/div/label/div/div[2]"


# Funções
def enviar_mensagem(mensagem):
    caixa_de_mensagem = driver.find_element_by_xpath(x_caixamsg)
    quebrado = mensagem.split('\n')
    for paragrafo in quebrado:
        caixa_de_mensagem.send_keys(paragrafo)
        caixa_de_mensagem.send_keys(Keys.SHIFT + Keys.ENTER)
    act.key_up(Keys.SHIFT).send_keys(Keys.ENTER).perform()


def checa_fixada(classe, local=driver):
    try:
        local.find_element_by_class_name(classe)
    except:
        return False
    else:
        return True


def espera_mensagem():
    ultima_mensagem = driver.find_elements_by_class_name(c_itenscv)[-1]
    ultima_mensagem_recebida = driver.find_elements_by_class_name('message-in')[-1]
    estrutura_msg = re.compile(r"([\w,\W]+)\n\d{2}:\d{2}")
    while ultima_mensagem != ultima_mensagem_recebida:
        sleep(1)
    msg_limpa = re.findall(estrutura_msg, ultima_mensagem.text)[0]
    return msg_limpa


# Nome e contato dos operadores iniciais
mocas = {"Vitória": "9999-9999", "Cecília": "8888-8888", "Bia": "7777-7777"}
mocos = {"Gabriel": "6666-6666", "Vinícius": "5555-5555"}

# Pra que as mensagens iniciais não resetem
primeira_vez_saudacao = True
primeira_vez_confirmacao = True

#  loop com try pra caso haja algum erro, recomeçar
while True:
    try:
        operadores = {**mocas, **mocos}
        # Iterando entre os operadores
        for operador, contato in operadores.items():
            # Configurações de mensagem
            if operador in mocas:
                pronomes = {'companheirx': 'companheira', 'x': 'a', 'elx': 'ela', 'dx': 'da'}
            else:
                pronomes = {'companheirx': 'companheiro', 'x': 'o', 'elx': 'ele', 'dx': 'do'}

            agora = datetime.now()
            if agora.hour > 18 or agora.hour < 6:
                buenos = 'Boa noite'
            elif 12 > agora.hour > 6:
                buenos = 'Bom dia'
            else:
                buenos = 'Boa tarde'

            # Mensagens iniciais
            if primeira_vez_saudacao:
                saudacao = f'''{buenos}! 
		Sua mensagem já foi encaminhada. 
                Caso seja urgente pode falar com {pronomes['elx']} pelo número: {contato}.'''
            else:
                pass


            ativacao = "Olá! Como posso ajudar? Caso haja dúvida, pode ver as opções na descrição do grupo.\n"

            # Procurando novas mensagens
            while True:
                try:
                    driver.execute_script("document.getElementById('pane-side').scrollTo(0,0)")
                    nova_mensagem = driver.find_element_by_xpath(f"//span[contains(@class, '{c_bolha}')]//ancestor::div[@class='{c_contato}']")
                except:
                    pass
                else:  # Mensagem encontrada
                    nova_mensagem.click()
                    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, x_caixamsg)))

                    if checa_fixada(c_fixada, nova_mensagem):  # Se for mensagem de adm
                        enviar_mensagem(ativacao)
                        espera_mensagem()

                        if espera_mensagem() == '1':  # Adicionar Operador
                            enviar_mensagem("O operador em questão:\n"
                                            "1: É uma moça\n"
                                            "2: É um moço")
                            espera_mensagem()

                            if espera_mensagem() == '1':
                                genero = mocas
                            else:
                                genero = mocos

                            enviar_mensagem('Qual o nome?')
                            espera_mensagem()
                            nome = espera_mensagem()

                            enviar_mensagem('Qual o número?')
                            espera_mensagem()
                            numero = espera_mensagem()

                            genero[nome] = numero

                            enviar_mensagem('Serviço concluído')

                        elif espera_mensagem() == '2':  # Remover operador
                            enviar_mensagem(
                                "Essa é a atual lista de operadores. Quem você quer remover?\n"
                                "Digite exatamente como escrito na lista")
                            for op in operadores:
                                enviar_mensagem(op)
                            espera_mensagem()

                            if espera_mensagem() in mocas:
                                mocas.pop(espera_mensagem())
                            else:
                                mocos.pop(espera_mensagem())

                            enviar_mensagem('Serviço concluído')

                        elif espera_mensagem() == '3':  # Mudar mensagem de saudação
                            enviar_mensagem("Essa é a atual mensagem de saudação")
                            enviar_mensagem(saudacao)
                            enviar_mensagem("Como será a nova mensagem?")
                            espera_mensagem()

                            saudacao = espera_mensagem()

                            enviar_mensagem('Serviço concluído')
                            primeira_vez_saudacao = False

                        elif espera_mensagem() == '4':  # Mudar mensagem de confirmação
                            enviar_mensagem("Essa é a atual mensagem de confirmação")
                            enviar_mensagem(confirmacao)
                            enviar_mensagem("Como será a nova mensagem?")
                            espera_mensagem()

                            confirmacao = espera_mensagem()

                            enviar_mensagem('Serviço concluído')
                            primeira_vez_confirmacao = False

                        else:
                            enviar_mensagem('Opção não disponível. Tente de novo')

                    else:  # Se não for mensagem de adm
                        sauce = driver.page_source
                        soup = BeautifulSoup(sauce, 'html.parser')

                        # Análise da conversa e limpeza dos dados
                        mensagens_recebidas = driver.find_elements_by_class_name(c_recebidas)
                        mensagens_enviadas = driver.find_elements_by_class_name(c_enviadas)
                        numero_contato = soup.find('header', {'class': c_cabecalho}).find('span', {'class': c_numaberto}).text
                        sleep(1)

                        estrutura = re.compile(r"([\w,\W]+)\n(\d{2}:\d{2})")
                        ultima = mensagens_recebidas[-1].text
                        limpa = re.sub(r"Você\n[^\\\n]+\n", '', ultima)
                        horario = re.findall(estrutura, limpa)[0][1]
                        conteudo = re.findall(estrutura, limpa)[0][0]  # Horario e conteudo da ultima mensagem recebida

                        # Relatório
                        with io.open("relatorio.csv", "a", encoding="utf-8")as relatorio:
                            dados = f'{numero_contato}, {conteudo}, {agora.day}, {horario}, {operador}\n'
                            relatorio.write(dados)
                        sleep(1)

                        # Enviando mensagem pro remetente
                        if len(mensagens_enviadas) == 0:
                            enviar_mensagem(saudacao)
                        elif len(mensagens_enviadas) == 1:
                            enviar_mensagem(confirmacao)
                        else:
                            pass

                        # Enviando mensagem pro operador
                        caixa_de_pesquisa = driver.find_element_by_class_name(x_caixapesq)
                        caixa_de_pesquisa.click()
                        caixa_de_pesquisa.send_keys(contato)
                        sleep(2)
                        caixa_de_pesquisa.send_keys(Keys.ARROW_DOWN)
                        caixa_de_pesquisa.send_keys(Keys.ENTER)
                        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, x_caixamsg)))
                        enviar_mensagem(f'*NOVO CONTATO*: {numero_contato}\n'
                                        f'*MENSAGEM:*: {conteudo}')
                break
    except:
        pass
