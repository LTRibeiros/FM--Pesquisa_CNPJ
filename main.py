from shlex import quote
from selenium import webdriver
import pandas as pd



setor = input("setor da empresa:")
lugar = input("lugar da pesquisa:")

query = quote(f"empresas de {setor} em {lugar}")
url = f"https://www.google.com/maps/search/{query}"

#abrir o navegador
navegador = webdriver.Chrome()

navegador.get(url)
#tela cheia
navegador.fullscreen_window()

# selecionar um elemento na tela (no caso, a empresa na aba lateral)
div_empresa = navegador.find_elements("class name", "hfpxzc") #ou selecionar vários em uma lista
div_numeros = navegador.find_elements("class name", "UsdlK")  # pega os numeros

nome_empresas = []
numero_empresas = [numero.text for numero in div_numeros]


for div in div_empresa:
    nome_empresa = div.get_attribute("aria-label")#pega o nome da empresa, como atributo "aria-label" da div_empresa que foi localizada por classe
    nome_empresas.append(nome_empresa)


df = pd.DataFrame({
    'Nome da Empresa': nome_empresas,
    'Telefone': numero_empresas
})
df.to_csv("empresas.csv", index=False, encoding='utf-8-sig')




