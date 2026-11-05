import pandas as pd

df = pd.read_excel("JBSS32_evolucao.xlsx")
#Selecionando a coluna "valor" e aplicando funções
print(df["valor"].max())
print(df["valor"].min())
print(df["valor"].mean())
print(df["valor"].std())
#Selecionar linhas
print(df[0:1])
#selecionar linhas e colunas
colunas = ["conta", "valor"]
print(df[23:24][colunas])
#filtrar linhas atraves valor
linhas = df["trimestre"] == '20262T'
colunas = ["conta", "valor"]
print(df[linhas][colunas])
#linha
linhas = df["conta"] == "lucro"
colunas = ["valor"]
print(df[linhas][colunas].mean())
#Graficos
import seaborn as sns
import matplotlib.pyplot as plt
#Graficos do lucro
linhas = df["conta"] == "lucro"
colunas = ["trimestre", "valor"]
dados = df[linhas][colunas]
sns.lineplot(dados, x="trimestre", y="valor")
plt.title("Gráfico de lucro da JBS")
plt.xticks(rotation=45)
plt.show()
