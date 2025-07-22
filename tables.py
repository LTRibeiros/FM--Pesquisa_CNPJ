from idlelib.iomenu import encoding

import pandas as pd

empresas = pd.read_csv('empresas.csv')
cnpj_empresas = pd.read_csv('cnpj_empresas.csv')

df_final = pd.concat([empresas, cnpj_empresas], axis=1)
df_final.to_csv('Prospeccao.csv', index=False, encoding='utf-8-sig')
