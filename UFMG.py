from bs4 import BeautifulSoup
import requests

while True:
    try:
        url = 'https://ufmg.br/cursos/graduacao/'
        resultado = requests.get(url)

        print(resultado.status_code)
        soup = BeautifulSoup(resultado.content, 'html.parser')
        cursos = soup.find_all('a', {"class": "drop__link--accordion"})
        links = soup.find_all('a', {'class': 'drop__link'})
        uteis = tudo = []

        print('\033[1mCURSOS:\033[m')
        for curso in cursos:
            print(f'    {curso.text.capitalize()}')

        for link in links:
            if link['href'] != '#':
                uteis.append('https://ufmg.br' + link['href'])

        print('')
        print('\033[1mDISCIPLINAS OBRIGATÓRIAS:\033[m')
        for util in uteis:
            while True:
                try:
                    roda = requests.get(util)
                    rodona = BeautifulSoup(roda.content, 'html.parser')
                except:
                    continue
                else:
                    materias = rodona.find_all('a', {'class': 'drop__link--underlined'})
                    break
            for materia in materias:
                tudo.append(materia.text)
                if materia.text not in tudo:
                    print(f'    {materia.text}')
    except:
        continue
    else:
        break
