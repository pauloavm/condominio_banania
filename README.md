# Dashboard de Análise de Desempenho de Administradoras de Condomínio

🌐 **Demo online:** [https://condominios.streamlit.app/](https://condominios.streamlit.app/)

Este projeto consiste em uma solução de análise de dados ponta a ponta para o setor de administração de condomínios. Ele utiliza dados fictícios gerados proceduralmente para simular os principais fluxos de trabalho e métricas de desempenho (KPIs) de uma administradora, apresentando-os em um dashboard interativo construído com Streamlit.

## 🎯 Problema de Negócio

A gestão de condomínios é um setor complexo, com múltiplos fluxos de dados (financeiros, operacionais, de comunicação) que, se não forem bem geridos, podem levar a ineficiências e baixa satisfação dos clientes. Este projeto simula um ambiente de dados real para demonstrar como uma abordagem "data-driven" pode transformar a gestão reativa em uma estratégia proativa e baseada em evidências.

## ✨ Funcionalidades do Dashboard

O dashboard interativo permite que analistas, síndicos e gestores explorem as seguintes análises:

- **Saúde Financeira**: Visão consolidada e por condomínio de métricas como **Taxa de Inadimplência** e **Fluxo de Caixa Mensal**.
- **Eficiência Operacional**: Análise do **Tempo Médio de Resolução de Ocorrências** dos moradores e a proporção de **Manutenções Preventivas** vs. Corretivas.
- **Análise Combinada**: Um gráfico de dispersão que correlaciona a **inadimplência** com o **tempo de resolução de ocorrências**, ajudando a identificar se a insatisfação com o serviço impacta o pagamento das taxas.
- **Filtros Interativos**: Possibilidade de filtrar os dados por **Ano**, **Trimestre** e **Condomínio Específico** para uma análise granular.
- **Responsividade**: Layout otimizado para visualização em diferentes dispositivos (desktop e mobile).

## 🚀 Como Executar o Projeto: Um Guia Completo

Siga os passos abaixo em ordem para rodar o projeto em sua máquina local.

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.9+** instalado em seu sistema.

### 2. Clonar o Repositório

Abra seu terminal ou prompt de comando e clone o projeto do GitHub:

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
````

*Substitua `seu-usuario/seu-repositorio.git` pelo caminho real do seu repositório.*

### 3\. Configurar o Ambiente Virtual

É uma prática recomendada usar um ambiente virtual para gerenciar as dependências do projeto, evitando conflitos com outras instalações de Python.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows
venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 4\. Instalar as Dependências

Instale todas as bibliotecas necessárias para o projeto usando o arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

> **Conteúdo do `requirements.txt`**
>
> Para que o projeto funcione corretamente, seu arquivo `requirements.txt` deve conter apenas as seguintes bibliotecas:
>
> ```
> streamlit
> pandas
> plotly
> Faker
> ```

### 5\. Gerar os Dados Fictícios (Etapa Obrigatória)

**Importante:** O dashboard depende de dois arquivos CSV para funcionar. Você deve gerá-los antes de executar o aplicativo.

Execute o script de geração de dados no seu terminal:

```bash
python gerador_dados.py
```

*Siga as instruções no terminal para definir o número de condomínios e o período da simulação. Ao final da execução, dois arquivos (`dados_financeiros_condominios.csv` e `dados_operacionais_condominios.csv`) serão criados na pasta do projeto.*

### 6\. Executar o Dashboard

Com os dados gerados, inicie o aplicativo Streamlit.

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão (`http://localhost:8501`).

## 📁 Estrutura do Projeto

A pasta do seu projeto deve seguir a seguinte estrutura após a geração dos dados:

```
seu-repositorio/
├── app.py                  # Código do dashboard Streamlit
├── gerador_dados.py        # Código para gerar os datasets
├── requirements.txt        # Dependências do projeto
├── dados_financeiros_condominios.csv  # Dataset de dados financeiros
└── dados_operacionais_condominios.csv # Dataset de dados operacionais
```

## 🛠 Tecnologias Utilizadas

  - **Python**: Linguagem de programação principal.
  - **Pandas**: Para manipulação e análise de dados.
  - **Faker**: Para a geração de dados fictícios realistas.
  - **Streamlit**: Para a construção do dashboard interativo.
  - **Plotly Express**: Para a criação de visualizações de dados dinâmicas e responsivas.

## 🤝 Contribuição

Contribuições são bem-vindas\! Se você encontrar um bug, tiver uma ideia para uma nova funcionalidade ou quiser melhorar o código, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

Feito com muito ☕ por pauloavm
