import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página e Título
st.set_page_config(layout="wide", page_title="Análise de Gestão de Condomínios")
st.title("Dashboard de Análise de Desempenho de Condomínios")
st.write("---")


# 2. Carregamento e Preparação dos Dados
@st.cache_data
def load_data():
    """Carrega e prepara os datasets, unindo-os."""
    try:
        df_financeiro = pd.read_csv("dados_financeiros_condominios.csv")
        df_operacional = pd.read_csv("dados_operacionais_condominios.csv")

        # Conversão de datas e extração de Ano/Trimestre para o dataset financeiro
        df_financeiro["Data_Mes_Referencia"] = pd.to_datetime(
            df_financeiro["Data_Mes_Referencia"]
        )
        df_financeiro["Ano"] = df_financeiro["Data_Mes_Referencia"].dt.year
        df_financeiro["Trimestre"] = df_financeiro["Data_Mes_Referencia"].dt.quarter

        # Mescla os dois datasets usando ID_Condominio como chave para adicionar 'Nome_Condominio' aos dados operacionais
        # Usa 'left join' para manter todas as informações financeiras.
        df_completo = pd.merge(
            df_financeiro, df_operacional, on="ID_Condominio", how="left"
        )

        # Converte a coluna de data operacional para datetime
        df_completo["Data_Criacao"] = pd.to_datetime(df_completo["Data_Criacao"])

        return df_completo
    except FileNotFoundError:
        st.error(
            "Erro: Arquivos de dados não encontrados. Por favor, execute o script de geração de dados antes."
        )
        st.stop()


df_completo = load_data()

# 3. Sidebar para Filtros (Garante responsividade)
st.sidebar.header("Filtros de Análise")

# Filtro por Ano
anos_disponiveis = sorted(df_completo["Ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione o(s) Ano(s):", options=anos_disponiveis, default=anos_disponiveis
)

# Filtro por Trimestre
trimestres_disponiveis = sorted(df_completo["Trimestre"].unique())
trimestres_selecionados = st.sidebar.multiselect(
    "Selecione o(s) Trimestre(s):",
    options=trimestres_disponiveis,
    default=trimestres_disponiveis,
)

# Filtro por Condomínio
condominios_disponiveis = sorted(df_completo["Nome_Condominio"].unique())
condominio_selecionado = st.sidebar.selectbox(
    "Selecione um Condomínio:", options=["Todos"] + condominios_disponiveis
)

# 4. Aplicação dos Filtros
df_filtrado = df_completo[
    (df_completo["Ano"].isin(anos_selecionados))
    & (df_completo["Trimestre"].isin(trimestres_selecionados))
]

if condominio_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Nome_Condominio"] == condominio_selecionado]

# 5. KPIs Principais
col1, col2, col3, col4 = st.columns(4)

# KPI 1: Taxa de Inadimplência Média
taxa_inadimplencia_media = df_filtrado["Percentual_Inadimplencia"].mean()
col1.metric("Taxa de Inadimplência Média", f"{taxa_inadimplencia_media:.2f}%")

# KPI 2: Fluxo de Caixa Total
fluxo_de_caixa_total = df_filtrado["Fluxo_de_Caixa_Mensal"].sum()
col2.metric(
    "Fluxo de Caixa Total",
    f"R$ {fluxo_de_caixa_total:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
)

# KPI 3: Média de Tempo de Resolução de Ocorrências
media_tempo_resolucao = df_filtrado[df_filtrado["Tipo_Registro"] == "Ocorrencia"][
    "Tempo_Resolucao_Horas"
].mean()
col3.metric("Tempo Médio de Resolução", f"{media_tempo_resolucao:.2f} horas")

# KPI 4: Proporção de Manutenções Preventivas
manutencoes_preventivas = df_filtrado[
    df_filtrado["Tipo_Manutencao"] == "Preventiva"
].shape[0]
total_manutencoes = df_filtrado[df_filtrado["Tipo_Registro"] == "Manutencao"].shape[0]
proporcao_preventivas = (
    (manutencoes_preventivas / total_manutencoes) * 100 if total_manutencoes > 0 else 0
)
col4.metric("Manutenções Preventivas", f"{proporcao_preventivas:.2f}% do total")


# 6. Gráficos e Análises
st.write("---")
st.header("Análise Financeira por Condomínio")

# Novo Gráfico 1: Fluxo de Caixa Médio por Condomínio (Gráfico de Barras)
df_fluxo_caixa_condo = (
    df_filtrado.groupby("Nome_Condominio")["Fluxo_de_Caixa_Mensal"].mean().reset_index()
)
fig_fluxo_caixa_barras = px.bar(
    df_fluxo_caixa_condo,
    x="Nome_Condominio",
    y="Fluxo_de_Caixa_Mensal",
    title="Fluxo de Caixa Médio por Condomínio",
    labels={"Fluxo_de_Caixa_Mensal": "Fluxo de Caixa Médio (R$)"},
)
st.plotly_chart(fig_fluxo_caixa_barras, use_container_width=True)

# Novo Gráfico 2: Fluxo de Caixa Mensal por Condomínio (Facetado)
# A lógica de facetamento será aplicada apenas aos 8 condomínios com maior média de fluxo de caixa para evitar o erro.
df_top_condos_fluxo_caixa = (
    df_filtrado.groupby("Nome_Condominio")["Fluxo_de_Caixa_Mensal"]
    .mean()
    .nlargest(8)
    .index
)
df_filtrado_top_condos = df_filtrado[
    df_filtrado["Nome_Condominio"].isin(df_top_condos_fluxo_caixa)
]

if not df_filtrado_top_condos.empty:
    fig_fluxo_caixa_facet = px.line(
        df_filtrado_top_condos,
        x="Data_Mes_Referencia",
        y="Fluxo_de_Caixa_Mensal",
        facet_col="Nome_Condominio",
        facet_col_wrap=2,
        title="Fluxo de Caixa Mensal por Condomínio (Tendência Individual dos Top 8)",
        labels={
            "Data_Mes_Referencia": "Data",
            "Fluxo_de_Caixa_Mensal": "Fluxo de Caixa (R$)",
        },
    )
    fig_fluxo_caixa_facet.for_each_annotation(
        lambda a: a.update(text=a.text.split("=")[-1])
    )
    st.plotly_chart(fig_fluxo_caixa_facet, use_container_width=True)
else:
    st.warning(
        "Não há dados de fluxo de caixa para os condomínios selecionados nos filtros para esta análise."
    )

# Gráfico 3: Inadimplência por Condomínio (mantido)
df_inadimplencia_condo = (
    df_filtrado.groupby("Nome_Condominio")["Percentual_Inadimplencia"]
    .mean()
    .reset_index()
)
fig_inadimplencia = px.bar(
    df_inadimplencia_condo,
    x="Nome_Condominio",
    y="Percentual_Inadimplencia",
    title="Taxa Média de Inadimplência por Condomínio",
)
fig_inadimplencia.update_layout(
    xaxis_title="Condomínio", yaxis_title="Inadimplência Média (%)"
)
st.plotly_chart(fig_inadimplencia, use_container_width=True)

st.write("---")
st.header("Análise Operacional e de Clientes")

# Gráfico 4: Tempo Médio de Resolução de Ocorrências por Condomínio (mantido)
df_tempo_resolucao_condo = (
    df_filtrado[df_filtrado["Tipo_Registro"] == "Ocorrencia"]
    .groupby("Nome_Condominio")["Tempo_Resolucao_Horas"]
    .mean()
    .reset_index()
)
fig_tempo_resolucao = px.bar(
    df_tempo_resolucao_condo,
    x="Nome_Condominio",
    y="Tempo_Resolucao_Horas",
    title="Tempo Médio de Resolução de Ocorrências por Condomínio",
)
fig_tempo_resolucao.update_layout(
    xaxis_title="Condomínio", yaxis_title="Tempo em Horas"
)
st.plotly_chart(fig_tempo_resolucao, use_container_width=True)

# Gráfico 5: Tipos de Ocorrências (mantido)
df_ocorrencias_tipo = (
    df_filtrado[df_filtrado["Tipo_Registro"] == "Ocorrencia"]["Descricao"]
    .value_counts()
    .reset_index()
)
df_ocorrencias_tipo.columns = ["Descricao", "Count"]
fig_ocorrencias = px.pie(
    df_ocorrencias_tipo,
    names="Descricao",
    values="Count",
    title="Distribuição dos Tipos de Ocorrências",
)
st.plotly_chart(fig_ocorrencias, use_container_width=True)

# 7. Análise Combinada
st.write("---")
st.header("Análise Combinada: O Impacto da Operação nas Finanças")

# Gráfico 6: Inadimplência vs. Tempo de Resolução (mantido)
# Agrupa por Nome_Condominio para a análise de correlação
df_combinado_analise = (
    df_filtrado.groupby("Nome_Condominio")
    .agg(
        Media_Inadimplencia=("Percentual_Inadimplencia", "mean"),
        Media_Tempo_Resolucao=("Tempo_Resolucao_Horas", "mean"),
    )
    .reset_index()
)

if not df_combinado_analise.empty:
    fig_correlacao = px.scatter(
        df_combinado_analise,
        x="Media_Tempo_Resolucao",
        y="Media_Inadimplencia",
        color="Nome_Condominio",
        title="Correlação: Inadimplência x Tempo de Resolução de Ocorrências",
    )
    fig_correlacao.update_layout(
        xaxis_title="Tempo de Resolução (horas)", yaxis_title="Inadimplência (%)"
    )
    st.plotly_chart(fig_correlacao, use_container_width=True)
else:
    st.warning(
        "Não há dados operacionais e financeiros coincidentes para os filtros selecionados para esta análise combinada."
    )
