# ==========================================================
# EVOLLUTION SOCCER PRO 4.0
# Sistema Profissional de Análise de Jogos
# Poisson + Fair Odds + Value Bet + Kelly
# Autor: Raí Leon + Jarvas
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import poisson

# ----------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------

st.set_page_config(
    page_title="EVOLLUTION SOCCER PRO 4.0",
    layout="wide"
)

st.title("⚽ EVOLLUTION SOCCER PRO 4.0")
st.markdown("Modelo Estatístico Profissional para Trade Esportivo")

# ----------------------------------------------------------
# CARREGAR BASE
# ----------------------------------------------------------

@st.cache_data
def carregar_dados():

    df = pd.read_csv("data/brasileirao_2024_2025.csv")

    return df

df = carregar_dados()

# ----------------------------------------------------------
# PADRONIZAÇÃO DE TIMES
# ----------------------------------------------------------

mapa_times = {

"Vasco da Gama Saf":"Vasco",
"Atlético Mineiro Saf":"Atlético MG",
"Red Bull Bragantino":"Bragantino",
"Athletico Paranaense":"Athletico PR",
"Cuiabá Saf":"Cuiabá",
"Bahia Saf":"Bahia",
"Fluminense FC":"Fluminense"

}

df["mandante"] = df["mandante"].replace(mapa_times)
df["visitante"] = df["visitante"].replace(mapa_times)

# ----------------------------------------------------------
# PESO PARA TEMPORADA
# ----------------------------------------------------------

df["peso"] = df["ano"].apply(lambda x: 1.5 if x == 2025 else 1)

# ----------------------------------------------------------
# MÉDIAS DO CAMPEONATO
# ----------------------------------------------------------

media_gols_casa = df["gols_m"].mean()
media_gols_fora = df["gols_v"].mean()

# ----------------------------------------------------------
# LISTA DE TIMES
# ----------------------------------------------------------

times = sorted(list(set(df["mandante"].unique())))

# ----------------------------------------------------------
# SELEÇÃO DE JOGO
# ----------------------------------------------------------

st.sidebar.title("🎮 Simulador de Jogo")

mandante = st.sidebar.selectbox(
"Time Mandante",
times
)

visitante = st.sidebar.selectbox(
"Time Visitante",
times
)

# ----------------------------------------------------------
# FUNÇÃO FORÇA DOS TIMES
# ----------------------------------------------------------

def calcular_forca(time):

    jogos_casa = df[df["mandante"] == time]
    jogos_fora = df[df["visitante"] == time]

    ataque_casa = jogos_casa["gols_m"].mean() / media_gols_casa
    defesa_casa = jogos_casa["gols_v"].mean() / media_gols_fora

    ataque_fora = jogos_fora["gols_v"].mean() / media_gols_fora
    defesa_fora = jogos_fora["gols_m"].mean() / media_gols_casa

    return ataque_casa, defesa_casa, ataque_fora, defesa_fora

# ----------------------------------------------------------
# CALCULAR FORÇA
# ----------------------------------------------------------

ataque_casa, defesa_casa, _, _ = calcular_forca(mandante)
_, _, ataque_fora, defesa_fora = calcular_forca(visitante)

# ----------------------------------------------------------
# EXPECTATIVA DE GOLS
# ----------------------------------------------------------

exp_gols_casa = ataque_casa * defesa_fora * media_gols_casa
exp_gols_fora = ataque_fora * defesa_casa * media_gols_fora

# ----------------------------------------------------------
# MATRIZ POISSON
# ----------------------------------------------------------

max_gols = 6

matrix = np.zeros((max_gols,max_gols))

for i in range(max_gols):

    for j in range(max_gols):

        prob = poisson.pmf(i,exp_gols_casa) * poisson.pmf(j,exp_gols_fora)

        matrix[i][j] = prob

# ----------------------------------------------------------
# PROBABILIDADES
# ----------------------------------------------------------

prob_casa = np.sum(np.tril(matrix,-1))
prob_empate = np.sum(np.diag(matrix))
prob_fora = np.sum(np.triu(matrix,1))

# ----------------------------------------------------------
# EXIBIR PROBABILIDADES
# ----------------------------------------------------------

st.subheader("📊 Probabilidades do Modelo")

col1,col2,col3 = st.columns(3)

col1.metric("Casa",f"{prob_casa*100:.1f}%")
col2.metric("Empate",f"{prob_empate*100:.1f}%")
col3.metric("Fora",f"{prob_fora*100:.1f}%")

# ----------------------------------------------------------
# FAIR ODDS
# ----------------------------------------------------------

fair_casa = 1/prob_casa
fair_empate = 1/prob_empate
fair_fora = 1/prob_fora

st.subheader("🎯 Fair Odds")

col1,col2,col3 = st.columns(3)

col1.metric("Casa",f"{fair_casa:.2f}")
col2.metric("Empate",f"{fair_empate:.2f}")
col3.metric("Fora",f"{fair_fora:.2f}")

# ----------------------------------------------------------
# ODDS DO MERCADO
# ----------------------------------------------------------

st.subheader("📊 Inserir Odds do Mercado")

col1,col2,col3 = st.columns(3)

odd_casa = col1.number_input("Odd Casa",1.01,20.0,2.00)
odd_empate = col2.number_input("Odd Empate",1.01,20.0,3.50)
odd_fora = col3.number_input("Odd Fora",1.01,20.0,4.00)

# ----------------------------------------------------------
# VALUE BET
# ----------------------------------------------------------

valor_casa = odd_casa/fair_casa
valor_empate = odd_empate/fair_empate
valor_fora = odd_fora/fair_fora

st.subheader("💎 Índice de Valor")

col1,col2,col3 = st.columns(3)

col1.metric("Casa",f"{valor_casa:.2f}")
col2.metric("Empate",f"{valor_empate:.2f}")
col3.metric("Fora",f"{valor_fora:.2f}")

# ----------------------------------------------------------
# KELLY CRITERION
# ----------------------------------------------------------

st.subheader("💰 Kelly Stake")

banca = st.number_input("Banca disponível",10,100000,300)

def kelly(prob,odd):

    b = odd-1

    k = (prob*(b+1)-1)/b

    if k < 0:

        return 0

    return k

stake_casa = banca*kelly(prob_casa,odd_casa)
stake_empate = banca*kelly(prob_empate,odd_empate)
stake_fora = banca*kelly(prob_fora,odd_fora)

col1,col2,col3 = st.columns(3)

col1.metric("Stake Casa",f"R$ {stake_casa:.2f}")
col2.metric("Stake Empate",f"R$ {stake_empate:.2f}")
col3.metric("Stake Fora",f"R$ {stake_fora:.2f}")

# ----------------------------------------------------------
# HEATMAP DE PLACARES
# ----------------------------------------------------------

st.subheader("🔥 Probabilidade de Placar")

fig = px.imshow(
matrix,
labels=dict(x="Gols Visitante",y="Gols Mandante",color="Probabilidade"),
text_auto=True
)

st.plotly_chart(fig,use_container_width=True)

# ----------------------------------------------------------
# TOP PLACARES
# ----------------------------------------------------------

placares = []

for i in range(max_gols):

    for j in range(max_gols):

        placares.append({

            "Placar":f"{i} x {j}",
            "Probabilidade":matrix[i][j]

        })

df_placar = pd.DataFrame(placares)

df_placar = df_placar.sort_values(
"Probabilidade",
ascending=False
).head(10)

st.subheader("🏆 Placares Mais Prováveis")

st.dataframe(df_placar)

# ----------------------------------------------------------
# GRÁFICO PROBABILIDADE
# ----------------------------------------------------------

fig = go.Figure()

fig.add_bar(
x=["Casa","Empate","Fora"],
y=[prob_casa,prob_empate,prob_fora]
)

st.subheader("📈 Distribuição de Probabilidade")

st.plotly_chart(fig,use_container_width=True)

# ----------------------------------------------------------
# RESUMO DO MODELO
# ----------------------------------------------------------

st.subheader("📋 Diagnóstico do Jogo")

if valor_casa > 1.05:

    st.success("Value Bet detectado na vitória do mandante")

elif valor_fora > 1.05:

    st.success("Value Bet detectado na vitória visitante")

elif valor_empate > 1.05:

    st.success("Value Bet detectado no empate")

else:

    st.warning("Nenhum value bet encontrado")

# ----------------------------------------------------------
# FIM
# ----------------------------------------------------------