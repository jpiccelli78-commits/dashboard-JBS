import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Dashboard JBS", layout="wide")

df = pd.read_excel("JBSS32_evolucao.xlsx")
df_ind = pd.read_excel("JBSS32_indicadores.xlsx")
df_b3 = pd.read_excel("planilhao_b3.xlsx")

st.title("Dashboard da empresa JBS")
st.write("Análise da evolução financeira da JBS (JBSS32) e comparação com as empresas da B3.")

#Números do último trimestre
linhas = df["trimestre"] == "20262T"
dados_ultimo = df[linhas]
receita = dados_ultimo[dados_ultimo["conta"] == "receita"]["valor"].sum()
lucro = dados_ultimo[dados_ultimo["conta"] == "lucro"]["valor"].sum()
ebit = dados_ultimo[dados_ultimo["conta"] == "ebit"]["valor"].sum()
jbs = df_b3[df_b3["ticker"] == "JBSS32"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita (R$ mil)", f"{receita:,.0f}".replace(",", "."))
col2.metric("Lucro (R$ mil)", f"{lucro:,.0f}".replace(",", "."))
col3.metric("EBIT (R$ mil)", f"{ebit:,.0f}".replace(",", "."))
col4.metric("Preço da ação (R$)", f"{jbs['preco'].iloc[0]:.2f}")

tab1, tab2, tab3 = st.tabs(["Evolução", "Indicadores", "Planilhão B3"])

with tab1:
    #Escolher a conta para o gráfico
    conta = st.selectbox("Escolha a conta:", df["conta"].unique())
    linhas = df["conta"] == conta
    colunas = ["trimestre", "valor"]
    dados = df[linhas][colunas]
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(dados, x="trimestre", y="valor", marker="o", color="black")
    ax.set_title("Gráfico de " + conta + " da JBS")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    c1, c2, c3 = st.columns(3)
    c1.metric("Máximo", f"{dados['valor'].max():,.0f}".replace(",", "."))
    c2.metric("Mínimo", f"{dados['valor'].min():,.0f}".replace(",", "."))
    c3.metric("Média", f"{dados['valor'].mean():,.0f}".replace(",", "."))
    st.dataframe(df)

with tab2:
    #Gráfico do ROE e ROC
    linhas = df_ind["conta"] != "endividamento"
    dados = df_ind[linhas]
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(dados, x="trimestre", y="valor", hue="conta", marker="o", palette=["black", "gray"])
    ax.set_title("ROE e ROC da JBS")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    #Gráfico do endividamento
    linhas = df_ind["conta"] == "endividamento"
    dados = df_ind[linhas]
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(dados, x="trimestre", y="valor", color="black")
    ax.set_title("Endividamento da JBS")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    st.dataframe(df_ind)

with tab3:
    #Empresas do mesmo setor da JBS
    st.subheader("Empresas do setor de proteína")
    linhas = df_b3["setor"] == "proteína"
    colunas = ["ticker", "preco", "p_l", "p_vp", "roe", "margem_liquida", "dividend_yield"]
    setor = df_b3[linhas][colunas]
    st.dataframe(setor)
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(setor, x="ticker", y="roe", color="gray")
    ax.set_title("ROE das empresas do setor de proteína")
    st.pyplot(fig)
    #Número de empresas por setor
    st.subheader("Planilhão B3")
    st.dataframe(df_b3)
    df_size = df_b3.groupby("setor").size()
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(df_size, color="black")
    ax.set_title("Gráfico número de empresas por setor")
    plt.xticks(rotation=90)
    st.pyplot(fig)
