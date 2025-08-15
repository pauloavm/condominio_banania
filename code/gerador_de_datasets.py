import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Inicializando a Faker com várias localidades
locales = ["pt_BR"]
faker = Faker(locales)

# --- Modelos de Dados ---
# Tipos de despesas fixas e seus valores médios mensais (por unidade)
despesas_fixas_tipos = {
    "água": 1.5,  # Valor por unidade
    "energia_comum": 2.0,  # Valor por unidade
    "folha_de_pagamento": 10.0,  # Valor por unidade
    "serviços_gerais": 5.0,  # Valor por unidade
    "fundo_de_reserva": 5.0,  # Valor por unidade
    "seguro predial": 3.0,  # Valor por unidade
    "seguro do elevador": 1.0,  # Valor por unidade
    "limpeza": 4.0,  # Valor por unidade
}

# Tipos de ocorrências de moradores e seu tempo médio de resolução em horas
ocorrencias_tipos = {
    "reclamacao_barulho": (1, 48),  # Min, Max horas para resolução
    "problema_vazamento": (4, 120),
    "pedido_reparo_area_comum": (24, 168),
    "sugestao_melhoria": (1, 72),
    "reclamação_segurança": (0.5, 24),
    "aluguel de salão de festas": (0.5, 12),
    "aluguel de churrasqueira": (0.5, 17), 
    "outros": (1, 72),
}

# Tipos de manutenção (preventiva vs. corretiva)
manutencao_tipos = {
    "preventiva": 0.8,  # Probabilidade de ser preventiva
    "corretiva": 0.2,
}

# --- Funções de Geração de Dados ---


def generate_condominiums(num_condos):
    """Gera dados para um número de condomínios."""
    condominiums = []
    for i in range(1, num_condos + 1):
        condo_id = faker.uuid4()
        condo_name = f"Condomínio {faker.last_name()} Residence"
        num_units = random.randint(30, 200)
        cota_mensal_base = round(random.uniform(250.0, 800.0), 2)
        condominiums.append(
            {
                "ID_Condominio": str(condo_id),
                "Nome_Condominio": condo_name,
                "Total_Unidades": num_units,
                "Cota_Mensal_Base": cota_mensal_base,
            }
        )
    return condominiums


def generate_financial_records(condominiums, start_date, end_date):
    """Gera dados financeiros mensais para cada condomínio."""
    financial_records = []
    current_date = start_date
    record_id = 1

    while current_date <= end_date:
        for condo in condominiums:
            # Geração de receita (cota condominial)
            total_unidades = condo["Total_Unidades"]
            cota_mensal = condo["Cota_Mensal_Base"]

            # Simula a inadimplência com uma taxa variável
            inadimplentes_count = round(random.uniform(0.05, 0.20) * total_unidades)
            pagantes_count = total_unidades - inadimplentes_count

            receita_bruta = cota_mensal * total_unidades
            receita_liquida = cota_mensal * pagantes_count

            # Geração de despesas
            despesas_fixas_total = sum(
                total_unidades * valor for valor in despesas_fixas_tipos.values()
            )
            despesas_variaveis = round(random.uniform(0.0, 0.1) * receita_bruta, 2)

            total_despesas = round(despesas_fixas_total + despesas_variaveis, 2)

            fluxo_de_caixa = round(receita_liquida - total_despesas, 2)

            financial_records.append(
                {
                    "ID_Registro": record_id,
                    "ID_Condominio": condo["ID_Condominio"],
                    "Nome_Condominio": condo["Nome_Condominio"],
                    "Data_Mes_Referencia": current_date.strftime("%Y-%m"),
                    "Receita_Bruta_Mensal": receita_bruta,
                    "Receita_Liquida_Mensal": receita_liquida,
                    "Total_Unidades": total_unidades,
                    "Unidades_Inadimplentes": inadimplentes_count,
                    "Percentual_Inadimplencia": round(
                        (inadimplentes_count / total_unidades) * 100, 2
                    ),
                    "Total_Despesas_Mensal": total_despesas,
                    "Fluxo_de_Caixa_Mensal": fluxo_de_caixa,
                }
            )
            record_id += 1

        # Avança para o próximo mês
        current_date = current_date.replace(day=28) + timedelta(days=4)
        current_date = current_date.replace(day=1)

    return financial_records


def generate_operational_records(condominiums, num_records):
    """Gera dados sobre ocorrências e manutenções."""
    operational_records = []

    # Pool de moradores para simular clientes recorrentes
    residents_pool = []

    for i in range(1, num_records + 1):
        condo = random.choice(condominiums)

        # Simular um morador existente ou criar um novo
        if random.random() < 0.8 and residents_pool:
            resident = random.choice(residents_pool)
            if resident["ID_Condominio"] != condo["ID_Condominio"]:
                resident = generate_resident(condo)
                residents_pool.append(resident)
        else:
            resident = generate_resident(condo)
            residents_pool.append(resident)

        record_type = random.choice(["ocorrencia", "manutencao"])

        if record_type == "ocorrencia":
            ocorrencia_tipo = random.choice(list(ocorrencias_tipos.keys()))
            min_res, max_res = ocorrencias_tipos[ocorrencia_tipo]

            data_criacao = faker.date_time_between(
                start_date=datetime(2023, 1, 1), end_date="now"
            )
            tempo_resolucao = timedelta(hours=random.uniform(min_res, max_res))
            data_resolucao = data_criacao + tempo_resolucao

            operational_records.append(
                {
                    "ID_Registro": i,
                    "ID_Condominio": condo["ID_Condominio"],
                    "Tipo_Registro": "Ocorrencia",
                    "ID_Morador": resident["ID_Morador"],
                    "Nome_Morador": resident["Nome_Morador"],
                    "Unidade": resident["Unidade"],
                    "Descricao": ocorrencia_tipo.replace("_", " ").title(),
                    "Data_Criacao": data_criacao,
                    "Data_Resolucao": data_resolucao,
                    "Tempo_Resolucao_Horas": round(
                        tempo_resolucao.total_seconds() / 3600, 2
                    ),
                }
            )
        else:
            manutencao_tipo = (
                "Preventiva"
                if random.random() <= manutencao_tipos["preventiva"]
                else "Corretiva"
            )
            custo_manutencao = round(random.uniform(500, 10000), 2)

            operational_records.append(
                {
                    "ID_Registro": i,
                    "ID_Condominio": condo["ID_Condominio"],
                    "Tipo_Registro": "Manutencao",
                    "Descricao": f"Manutencao {manutencao_tipo.lower()} em área comum",
                    "Custo_Estimado": custo_manutencao,
                    "Tipo_Manutencao": manutencao_tipo,
                }
            )

    return operational_records


def generate_resident(condo):
    """Gera um morador para um condomínio específico."""
    return {
        "ID_Morador": faker.uuid4(),
        "Nome_Morador": faker.name(),
        "Unidade": random.randint(1, condo["Total_Unidades"]),
        "ID_Condominio": condo["ID_Condominio"],
    }


# --- Coleta de informações do usuário ---
num_condos_input = input("Insira o número de condomínios para a simulação: ")
num_records_input = input(
    "Insira a quantidade de registros operacionais (ocorrências/manutenções): "
)
year_start_input = input(
    "Insira o ano de início para a simulação financeira (ex: '2022'): "
)
year_end_input = input("Insira o ano de fim para a simulação financeira (ex: '2023'): ")

try:
    num_condos = int(num_condos_input) if num_condos_input.strip() else 5
    num_records = int(num_records_input) if num_records_input.strip() else 1000
    year_start = int(year_start_input) if year_start_input.strip() else 2022
    year_end = int(year_end_input) if year_end_input.strip() else datetime.now().year

    start_date = datetime(year_start, 1, 1)
    end_date = datetime(year_end, 12, 31)

except (ValueError, EOFError):
    num_condos = 5
    num_records = 1000
    start_date = datetime(2022, 1, 1)
    end_date = datetime.now()

# --- Geração dos Dados ---
condominiums_data = generate_condominiums(num_condos)

financial_data = generate_financial_records(condominiums_data, start_date, end_date)
df_financeiro = pd.DataFrame(financial_data)

operational_data = generate_operational_records(condominiums_data, num_records)
df_operacional = pd.DataFrame(operational_data)

# --- Salvar os DataFrames ---
nome_arquivo_financeiro = "dados_financeiros_condominios.csv"
nome_arquivo_operacional = "dados_operacionais_condominios.csv"

df_financeiro.to_csv(nome_arquivo_financeiro, index=False, encoding="utf-8")
df_operacional.to_csv(nome_arquivo_operacional, index=False, encoding="utf-8")

# --- Exibir Resultados ---
print(
    f"\nA base de dados financeira '{nome_arquivo_financeiro}' foi criada com sucesso com {len(df_financeiro)} registros."
)
print(
    f"A base de dados operacional '{nome_arquivo_operacional}' foi criada com sucesso com {len(df_operacional)} registros."
)

print("\nPrimeiras 5 linhas do DataFrame Financeiro:")
print(df_financeiro.head())

print("\nPrimeiras 5 linhas do DataFrame Operacional:")
print(df_operacional.head())
