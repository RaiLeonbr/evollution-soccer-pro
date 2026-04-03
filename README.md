# ⚽ Evollution Soccer Pro

Sistema de análise estatística para partidas de futebol utilizando **Python**, **modelagem probabilística** e **visualização interativa**.

O projeto utiliza dados históricos do **Campeonato Brasileiro Série A (2024–2025)** para calcular probabilidades de resultados, identificar **Value Bets**, calcular **Fair Odds** e sugerir stakes com o **Critério de Kelly**.

A aplicação foi construída com **Streamlit** para permitir análises rápidas e interativas.

---

# 📊 Funcionalidades

### 🔹 Análise de Confrontos

* Histórico de partidas entre os times selecionados
* Visualização dos resultados e placares

### 🔹 Probabilidades de Resultado

Cálculo de probabilidade para:

* Vitória do mandante
* Empate
* Vitória do visitante

Utilizando **modelagem estatística baseada em médias ofensivas e defensivas**.

---

### 🔹 📊 Fair Odds

O sistema calcula automaticamente as **odds justas** com base nas probabilidades estatísticas.

Exemplo:

| Resultado | Probabilidade | Fair Odd |
| --------- | ------------- | -------- |
| Casa      | 63%           | 1.58     |
| Empate    | 22%           | 4.54     |
| Fora      | 15%           | 6.66     |

---

### 🔹 💰 Kelly Criterion

Cálculo automático da **stake recomendada** com base em:

* Probabilidade estimada
* Odd da casa de apostas
* Bankroll disponível

Fórmula utilizada:

Kelly Criterion

```
f = (p × b − (1 − p)) / b
```

Onde:

* `p` = probabilidade estimada
* `b` = odd - 1

---

### 🔹 💹 Value Bet

O sistema identifica automaticamente oportunidades de **valor esperado positivo**.

Uma aposta é considerada **Value Bet** quando:

```
Odd da casa > Fair Odd
```

---

# 📈 Estatísticas utilizadas

O modelo considera:

### Ataque

Média de gols marcados

### Defesa

Média de gols sofridos

Separando:

* Jogos como **mandante**
* Jogos como **visitante**

Isso cria um modelo de **força ofensiva e defensiva** para cada equipe.

---

# 📂 Estrutura do Projeto

```
evollution-soccer-pro
│
├── streamlit_app.py
│
├── data
│   └── brasileirao_2024_2025.csv
│
├── requirements.txt
│
└── README.md
```

---

# 🧠 Tecnologias Utilizadas

* Python
* Pandas
* Streamlit
* Plotly
* Estatística aplicada ao esporte

---

# 🚀 Como executar o projeto

### 1️⃣ Clonar o repositório

```
git clone https://github.com/seu-usuario/evollution-soccer-pro.git
```

---

### 2️⃣ Entrar na pasta

```
cd evollution-soccer-pro
```

---

### 3️⃣ Instalar dependências

```
pip install -r requirements.txt
```

---

### 4️⃣ Executar a aplicação

```
streamlit run streamlit_app.py
```

---

# 📊 Exemplo do Dashboard

O sistema permite:

* Selecionar dois times
* Inserir odds do mercado
* Ver probabilidades estimadas
* Calcular fair odds
* Identificar value bets
* Sugerir stake com Kelly

---

# 📚 Modelo Estatístico

O projeto utiliza conceitos de:

* Probabilidade aplicada ao futebol
* Estatística descritiva
* Modelagem de odds
* Gestão de risco com Kelly Criterion

---

# 🎯 Objetivo do Projeto

Demonstrar a aplicação de **Ciência de Dados e Estatística no futebol**, criando uma ferramenta de apoio para análise de partidas e identificação de valor no mercado de odds.

---

# 👨‍💻 Autor

**Raí Leon**

Projeto desenvolvido para estudo de:

* Data Science
* Sports Analytics
* Modelagem probabilística
* Visualização de dados

---

# 📜 Licença

Este projeto é de uso educacional.
