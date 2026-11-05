import pandas as pd

df = pd.read_excel("JBSS32_evolucao.xlsx")
print(df.head())
print(df.columns)
colunas = ['conta', 'trimestre', 'valor']
print(df[colunas])


print(pd.read_excel("JBSS32_indicadores.xlsx"))
