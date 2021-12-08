import requests
from pprint import pprint

api = requests.get('https://pokeapi.co/api/v2/pokemon?limit=10&offset=193')
dados = api.json()
resultados = [dados['results']]
nomes = [nome['name'] for nome in resultados[0]]
print(nomes)