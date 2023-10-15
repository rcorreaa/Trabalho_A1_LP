import pandas as pd
import matplotlib.pyplot as plt
import doctest

def plot_grafico_stacked_bar(path_data, ini_ano=2018, fim_ano=2022, ax=None):
    """
    Cria um stacked bar com as proporções dos valores "Sem dispensa" e "Com dispensa" 
    da coluna DISPENSA em relação as regiões brasileiras dos anos de 2018 a 2022.

    Parameters:
        path_data(caminho): Caminho dos DataFrames.
        ini_ano(int): Ano de início. 2018 por padrão
        fim_ano(int): Ano de término. 2022 por padrão

    Returns:
        None

    Exemplos:
    Exemplo válido para um caminho com os anos corretos
    >>> plot_grafico_stacked_bar("C:/Users/samue/OneDrive/Documentos/Dados/", ini_ano=2018, fim_ano=2022)

    Exemplo inválido para um intervalo de anos onde não há dados
    >>> plot_grafico_stacked_bar("C:/Users/samue/OneDrive/Documentos/Dados/", ini_ano=2010, fim_ano=2018)
    Erro de leitura no database do ano 2010: [Errno 2] No such file or directory: 'C:/Users/samue/OneDrive/Documentos/Dados/sermil2010.csv'      
    """

    if ax is None:
        fig, ax = plt.subplots()

    v_df = []
    for ano in range(ini_ano, fim_ano+1):
        # Leitura do database com tratamento de erro
        try:
            df = pd.read_csv(path_data + "sermil{}.csv".format(ano), usecols=["UF_JSM", "DISPENSA", "VINCULACAO_ANO"], encoding="latin1")
        except Exception as e:
            print(f"Erro de leitura no database do ano {ano}: {e}")
            return

        v_df.append(df)
        
    # Juntando todos os DataFrames
    df_completo = pd.concat(v_df, ignore_index=True) 

    # Criando dicionário para mapear os estados
    mapeamento_regioes = {
        'AC': 'Norte',
        'AL': 'Nordeste',
        'AM': 'Norte',
        'AP': 'Norte',
        'BA': 'Nordeste',
        'CE': 'Nordeste',
        'DF': 'Centro-Oeste',
        'ES': 'Sudeste',
        'GO': 'Centro-Oeste',
        'MA': 'Nordeste',
        'MG': 'Sudeste',
        'MS': 'Centro-Oeste',
        'MT': 'Centro-Oeste',
        'PA': 'Norte',
        'PB': 'Nordeste',
        'PE': 'Nordeste',
        'PI': 'Nordeste',
        'PR': 'Sul',
        'RJ': 'Sudeste',
        'RN': 'Nordeste',
        'RO': 'Norte',
        'RR': 'Norte',
        'RS': 'Sul',
        'SC': 'Sul',
        'SE': 'Nordeste',
        'SP': 'Sudeste',
        'TO': 'Norte'
    }

    # Cria novo DataFrame com a coluna REGIAO
    df_completo["REGIAO"] = df_completo["UF_JSM"].map(mapeamento_regioes)
    df_agrupado = df_completo.groupby("REGIAO")["DISPENSA"].value_counts().reset_index()
    
    # Cria novo DataFrame com as proporções dos valores da DISPENSA
    somas = df_agrupado.groupby(["REGIAO", "DISPENSA"])["count"].sum()
    soma_total = df_agrupado.groupby("REGIAO")["count"].sum()
    proporcoes = somas.unstack().div(soma_total, axis=0).reset_index()
    proporcoes.columns = ["REGIAO", "Com dispensa", "Sem dispensa"]

    proporcoes["Com_dispensa_percent"] = proporcoes["Com dispensa"] * 100
    proporcoes["Sem_dispensa_percent"] = proporcoes["Sem dispensa"] * 100

    bar1 = plt.barh(proporcoes["REGIAO"], proporcoes["Com_dispensa_percent"], label="Com dispensa", color="#A50030")
    bar2 = plt.barh(proporcoes["REGIAO"], proporcoes["Sem_dispensa_percent"], left=proporcoes["Com_dispensa_percent"], label="Sem dispensa", color="#1A3071")

    ax.bar_label(bar1, fmt='%.2f%%', label_type="center", fontsize=10)
    ax.bar_label(bar2, fmt='%.2f%%', label_type="center", fontsize=10)

    ax.set_title("Proporção de alistados com e sem dispensas por Região")
    plt.legend()
    plt.show()
    return None

if __name__ == "__main__":
    doctest.testmod()