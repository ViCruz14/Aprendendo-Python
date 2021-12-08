import re
from matplotlib import pyplot as plt


with open(r'conversa.txt', encoding="utf8") as conversa:
    dados = conversa.read()

estrutura = re.compile("\d{2}/\d{2}/\d{4} \d{2}:\d{2} - ([^:]+): ")

nomes = re.findall(estrutura, dados)

contador = {}
for nome in nomes:
    if nome in contador.keys():
        contador[nome] += 1
    else:
        contador[nome] = 1

ordem = sorted(contador.items(), key=lambda x: x[1], reverse=True)
for i in ordem:
    print(f'{i[1]} - {i[0]}')

plt.bar(contador.keys(), contador.values())
plt.show()
