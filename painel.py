import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(page_title="Dashboard JBS", page_icon="📊", layout="wide")

# Cores do dashboard
AZUL = "#0B1F3A"
VERMELHO = "#C8102E"
CINZA = "#6B7280"

# Estilo visual (CSS) para deixar o painel mais elegante
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; }
.cabecalho {
    background: linear-gradient(90deg, #0B1F3A 0%, #1E3A5F 100%);
    padding: 28px 32px; border-radius: 14px; margin-bottom: 24px;
}
.cabecalho h1 { color: white; margin: 0; font-size: 2.1rem; font-weight: 700; }
.cabecalho p { color: #CBD5E1; margin: 6px 0 0 0; font-size: 1rem; }
.cartao {
    background: white; border: 1px solid #E5E7EB; border-left: 5px solid #C8102E;
    border-radius: 12px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.cartao .titulo { color: #6B7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }
.cartao .valor { color: #0B1F3A; font-size: 1.7rem; font-weight: 700; margin-top: 4px; }
.cartao .variacao { font-size: 0.85rem; margin-top: 2px; }
.positivo { color: #059669; }
.negativo { color: #DC2626; }
.secao { color: #0B1F3A; font-weight: 700; font-size: 1.25rem; margin: 10px 0 4px 0; }
.rodape { color: #9CA3AF; font-size: 0.8rem; text-align: center; margin-top: 40px; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Estilo dos gráficos
sns.set_theme(style="whitegrid")
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


# ---------------- LEITURA DOS DADOS ----------------
df = pd.read_excel("JBSS32_evolucao.xlsx")
df_ind = pd.read_excel("JBSS32_indicadores.xlsx")
df_b3 = pd.read_excel("planilhao_b3.xlsx")

# Transformar "20262T" em "2T26" (mais fácil de ler)
def formatar_trimestre(t):
    return t[4] + "T" + t[2:4]

df["periodo"] = df["trimestre"].apply(formatar_trimestre)
df_ind["periodo"] = df_ind["trimestre"].apply(formatar_trimestre)

# Valores em R$ bilhões (os dados vêm em R$ mil)
df["valor_bi"] = df["valor"] / 1_000_000

nomes_contas = {
    "receita": "Receita",
    "ebit": "EBIT",
    "lucro": "Lucro Líquido",
    "divida_liquida": "Dívida Líquida",
    "caixa_operac": "Caixa Operacional",
    "pl": "Patrimônio Líquido",
}
nomes_indicadores = {"roe": "ROE", "roc": "ROC", "endividamento": "Endividamento"}


# ---------------- FUNÇÕES AUXILIARES ----------------
trimestres = list(df["trimestre"].unique())
ultimo = trimestres[-1]
anterior = trimestres[-2]

def valor_conta(conta, trimestre):
    linhas = (df["conta"] == conta) & (df["trimestre"] == trimestre)
    return df[linhas]["valor_bi"].sum()

def cartao(titulo, valor, variacao=None):
    texto_var = ""
    if variacao is not None:
        classe = "positivo" if variacao >= 0 else "negativo"
        seta = "▲" if variacao >= 0 else "▼"
        texto_var = f'<div class="variacao {classe}">{seta} {variacao:+.1f}% vs. trimestre anterior</div>'
    st.markdown(f"""
    <div class="cartao">
        <div class="titulo">{titulo}</div>
        <div class="valor">{valor}</div>
        {texto_var}
    </div>
    """, unsafe_allow_html=True)

def variacao(conta):
    atual = valor_conta(conta, ultimo)
    antes = valor_conta(conta, anterior)
    return (atual - antes) / abs(antes) * 100

def grafico_linha(dados, titulo, cor=VERMELHO, rotulo_y="R$ bilhões"):
    fig, ax = plt.subplots(figsize=(12, 4.2))
    sns.lineplot(dados, x="periodo", y="valor_bi", marker="o", color=cor, linewidth=2.5, ax=ax)
    ax.fill_between(range(len(dados)), dados["valor_bi"], alpha=0.08, color=cor)
    ax.set_title(titulo, fontsize=14, fontweight="bold", color=AZUL, loc="left", pad=12)
    ax.set_xlabel("")
    ax.set_ylabel(rotulo_y, color=CINZA)
    plt.xticks(rotation=90, fontsize=8, color=CINZA)
    plt.yticks(color=CINZA)
    fig.tight_layout()
    return fig


# ---------------- BARRA LATERAL ----------------
with st.sidebar:
    st.markdown("## JBS S.A.")
    st.markdown("**Ticker:** JBSS32")
    st.markdown("**Setor:** Proteína animal")
    st.markdown("**Último trimestre:** " + formatar_trimestre(ultimo))
    st.divider()
    st.markdown("**Fonte dos dados:** planilhas da B3 fornecidas em aula.")
    st.caption("Valores financeiros em R$ bilhões.")


# ---------------- CABEÇALHO ----------------
st.markdown(f"""
<div class="cabecalho">
    <h1>Dashboard Financeiro — JBS</h1>
    <p>Evolução dos resultados, indicadores de rentabilidade e comparação com o mercado · Dados até o {formatar_trimestre(ultimo)}</p>
</div>
""", unsafe_allow_html=True)


# ---------------- CARTÕES (KPIs) ----------------
jbs = df_b3[df_b3["ticker"] == "JBSS32"]
c1, c2, c3, c4 = st.columns(4)
with c1:
    cartao("Receita", f"R$ {valor_conta('receita', ultimo):,.1f} bi", variacao("receita"))
with c2:
    cartao("Lucro Líquido", f"R$ {valor_conta('lucro', ultimo):,.1f} bi", variacao("lucro"))
with c3:
    cartao("EBIT", f"R$ {valor_conta('ebit', ultimo):,.1f} bi", variacao("ebit"))
with c4:
    cartao("Preço da ação", f"R$ {jbs['preco'].iloc[0]:.2f}")

st.write("")


# ---------------- ABAS ----------------
tab1, tab2, tab3 = st.tabs(["📈 Evolução", "📊 Indicadores", "🏢 Comparação B3"])

with tab1:
    st.markdown('<div class="secao">Evolução das contas</div>', unsafe_allow_html=True)
    conta = st.selectbox("Escolha a conta:", list(nomes_contas.keys()),
                         format_func=lambda c: nomes_contas[c])
    linhas = df["conta"] == conta
    dados = df[linhas][["periodo", "valor_bi"]].reset_index(drop=True)
    st.pyplot(grafico_linha(dados, nomes_contas[conta] + " por trimestre"))

    e1, e2, e3 = st.columns(3)
    with e1:
        cartao("Máximo", f"R$ {dados['valor_bi'].max():,.1f} bi")
    with e2:
        cartao("Mínimo", f"R$ {dados['valor_bi'].min():,.1f} bi")
    with e3:
        cartao("Média", f"R$ {dados['valor_bi'].mean():,.1f} bi")

    st.write("")
    with st.expander("Ver tabela completa"):
        tabela = df.pivot(index="periodo", columns="conta", values="valor_bi")
        tabela = tabela.reindex(df["periodo"].unique()).rename(columns=nomes_contas)
        st.dataframe(tabela.style.format("{:,.2f}"), use_container_width=True)

with tab2:
    st.markdown('<div class="secao">Indicadores de rentabilidade e endividamento</div>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    ult_ind = df_ind[df_ind["trimestre"] == ultimo]
    with i1:
        cartao("ROE", f"{ult_ind[ult_ind['conta'] == 'roe']['valor'].sum() * 100:.1f}%")
    with i2:
        cartao("ROC", f"{ult_ind[ult_ind['conta'] == 'roc']['valor'].sum() * 100:.1f}%")
    with i3:
        cartao("Endividamento", f"{ult_ind[ult_ind['conta'] == 'endividamento']['valor'].sum():.2f}x")

    st.write("")
    fig, ax = plt.subplots(figsize=(12, 4.2))
    rent = df_ind[df_ind["conta"].isin(["roe", "roc"])].copy()
    rent["conta"] = rent["conta"].map(nomes_indicadores)
    sns.lineplot(rent, x="periodo", y="valor", hue="conta", marker="o", linewidth=2.5,
                 palette=[VERMELHO, AZUL], ax=ax)
    ax.set_title("ROE e ROC por trimestre", fontsize=14, fontweight="bold", color=AZUL, loc="left", pad=12)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.legend(title="", frameon=False)
    plt.xticks(rotation=90, fontsize=8, color=CINZA)
    fig.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 3.6))
    endiv = df_ind[df_ind["conta"] == "endividamento"]
    sns.barplot(endiv, x="periodo", y="valor", color=AZUL, ax=ax)
    ax.set_title("Endividamento por trimestre", fontsize=14, fontweight="bold", color=AZUL, loc="left", pad=12)
    ax.set_xlabel("")
    ax.set_ylabel("vezes", color=CINZA)
    plt.xticks(rotation=90, fontsize=8, color=CINZA)
    fig.tight_layout()
    st.pyplot(fig)

with tab3:
    st.markdown('<div class="secao">JBS frente às empresas do setor de proteína</div>', unsafe_allow_html=True)
    linhas = df_b3["setor"] == "proteína"
    setor = df_b3[linhas][["ticker", "preco", "p_l", "p_vp", "roe", "margem_liquida", "dividend_yield"]]
    setor = setor.rename(columns={"ticker": "Empresa", "preco": "Preço (R$)", "p_l": "P/L", "p_vp": "P/VP",
                                  "roe": "ROE", "margem_liquida": "Margem Líquida",
                                  "dividend_yield": "Dividend Yield"})
    st.dataframe(setor.style.format({"Preço (R$)": "{:.2f}", "P/L": "{:.2f}", "P/VP": "{:.2f}",
                                     "ROE": "{:.1%}", "Margem Líquida": "{:.1%}",
                                     "Dividend Yield": "{:.1%}"}),
                 use_container_width=True, hide_index=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig, ax = plt.subplots(figsize=(6, 4))
        cores = [VERMELHO if t == "JBSS32" else "#CBD5E1" for t in setor["Empresa"]]
        sns.barplot(setor, x="Empresa", y="ROE", palette=cores, hue="Empresa", legend=False, ax=ax)
        ax.set_title("ROE no setor de proteína", fontsize=13, fontweight="bold", color=AZUL, loc="left")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.set_xlabel("")
        fig.tight_layout()
        st.pyplot(fig)
    with col_b:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(setor, x="Empresa", y="P/L", palette=cores, hue="Empresa", legend=False, ax=ax)
        ax.set_title("P/L no setor de proteína", fontsize=13, fontweight="bold", color=AZUL, loc="left")
        ax.set_xlabel("")
        fig.tight_layout()
        st.pyplot(fig)

    st.markdown('<div class="secao">Número de empresas por setor na B3</div>', unsafe_allow_html=True)
    df_size = df_b3.groupby("setor").size().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 4.2))
    cores_setor = [VERMELHO if s == "proteína" else AZUL for s in df_size.index]
    sns.barplot(x=df_size.index, y=df_size.values, palette=cores_setor, hue=df_size.index, legend=False, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("empresas", color=CINZA)
    plt.xticks(rotation=90, fontsize=9, color=CINZA)
    fig.tight_layout()
    st.pyplot(fig)

    with st.expander("Ver planilhão completo da B3"):
        st.dataframe(df_b3, use_container_width=True, hide_index=True)


# ---------------- RODAPÉ ----------------
st.markdown('<div class="rodape">Programação Estruturada · Ibmec · Dashboard desenvolvido em Python com Streamlit</div>',
            unsafe_allow_html=True)
