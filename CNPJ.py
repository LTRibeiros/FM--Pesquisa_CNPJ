import time
import pandas as pd
import urllib.parse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from main import nome_empresas  #lista de nomes

cnpjs = []
razao_empresas = []
status_empresas = []
local_empresas = []

for nome in nome_empresas:
    nome_codificado = urllib.parse.quote(nome)
    url = f"https://cnpj.biz/procura/{nome_codificado}"

    # Inicializa navegador com undetected_chromedriver
    options = uc.ChromeOptions()
    options.headless = False

    navegador = uc.Chrome(options=options, version_main=138)
    navegador.get(url)

    time.sleep(15)  # aguarda Cloudflare

    try:
        empresa_element = navegador.find_element(By.CSS_SELECTOR, "li a.block")

        # Extrair o nome da empresa
        nome_empresa = empresa_element.find_element(By.CSS_SELECTOR, "p.text-lg.font-medium.text-blue-600").text
        razao_empresas.append(nome_empresa)

        # Extrair o CNPJ (está dentro de um p que segue um svg)
        cnpj = empresa_element.find_element(By.XPATH, ".//p[contains(text(), '/')]").text
        cnpjs.append(cnpj
                     )
        estado_element = navegador.find_element(By.CSS_SELECTOR, "p.inline-flex.text-xs.leading-5")
        estado = estado_element.text.strip()  # Retorna "ATIVA" ou "BAIXADA"
        status_empresas.append(estado)

        localizacao = navegador.find_element(By.XPATH,".//p[contains(., 'SP') or contains(., 'RJ')]").text  # Adapte para outros estados
        local_empresas.append(localizacao)

        print(f"Nome: {nome_empresa}")
        print(f"CNPJ: {cnpj}")
        print(f"Estado: {estado}")
        print(f"Localização: {localizacao}")
        # time.sleep(5)
    except Exception as e:
        print(f"Não foi possivel encontrar o cnpj de {nome}")
        df = pd.read_csv("empresas.csv")

        df = df[~df["Nome da Empresa"].str.contains(nome, case=False, na=False)]

        df.to_csv("empresas.csv", index=False)

dfc = pd.DataFrame({
'CNPJ': cnpjs,
'Nome Social': razao_empresas,
'Status': status_empresas,
'Localização': local_empresas

})
dfc.to_csv("cnpj_empresas.csv", index=False, encoding='utf-8-sig')




