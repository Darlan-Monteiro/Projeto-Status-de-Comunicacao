import pandas as pd
from glob import glob
from dotenv import load_dotenv
import os

# Bloco para carregar os caminhos das variáveis de ambiente
load_dotenv()
caminho_bdrfv = os.getenv('caminho_bdrfv')
caminho_bdativos = os.getenv('caminho_bdativos')
caminho_ativosatt = os.getenv('caminho_ativosatt')

def ler_base():
    arquivos = sorted(glob(caminho_bdrfv))
    if not arquivos:
        print("Nenhum arquivo encontrado na pasta especificada.")
        return None
    arquivos_concat = pd.concat((pd.read_excel(cont, sheet_name='Current Comm Loss Status') for cont in arquivos), ignore_index=True)
    print(arquivos_concat)
    return arquivos_concat

def ler_planilha_ativos():
    caminho_ativos = caminho_bdativos
    aba_ativos = 'Ativos'
    try:
        planilha_ativos = pd.read_excel(caminho_ativos, sheet_name=aba_ativos)
        return planilha_ativos
    except ValueError:
        print(f"Arquivo {caminho_ativos} não encontrado.")
        return None

def remover_separador(separador):
    if isinstance(separador, str):
        return separador[-8:].strip()

def processar_dados():
    bases_concat = ler_base()
    ativos = ler_planilha_ativos()

    coluna_bdconcat = 'Asset Name'
    coluna_bdativos = 'NºSÉRIE'

    if bases_concat is None or ativos is None:
        print('Erro! Base de dados vazia')
        exit()

    if coluna_bdconcat not in bases_concat.columns or coluna_bdativos not in ativos.columns:
        print("Colunas não encontradas em um dos arquivos.")
        exit()

    asset_name_modificado = bases_concat[coluna_bdconcat].astype(str).apply(remover_separador)
    num_series = ativos[coluna_bdativos].astype(str)

    num_series_modificado = set()
    for num in num_series:
        partes = num.split('/')
        for serie in partes:
            num_series_modificado.add(serie.strip())

    lista_nao_contem = []
    for asset_name in asset_name_modificado:
        for n_serie in num_series_modificado:
            if asset_name in n_serie:
                print(f'{asset_name} está presente em NºSÉRIE')
                break
        else:
            print(f'{asset_name} NÃO está presente em NºSÉRIE')
            lista_nao_contem.append(asset_name)

 
    ativos['Data Última Comunicação'].replace(['-', '', 'NaT'], pd.NaT, inplace=True)
    ativos['Data Último Envio de Dados'].replace(['-', '', 'NaT'], pd.NaT, inplace=True)

    bases_concat['Last Update'] = pd.to_datetime(bases_concat['Last Update'], errors='coerce')
    bases_concat['Max Sample Time'] = pd.to_datetime(bases_concat['Max Sample Time'], errors='coerce')
    ativos['Data Última Comunicação'] = pd.to_datetime(ativos['Data Última Comunicação'], errors='coerce')
    ativos['Data Último Envio de Dados'] = pd.to_datetime(ativos['Data Último Envio de Dados'], errors='coerce')

    nao_atualizados_ultima_comunicacao = []
    nao_atualizados_ultimo_envio = []

    for i, linha in bases_concat.iterrows():
        asset_name = remover_separador(linha[coluna_bdconcat])
        last_update_date = linha['Last Update']
        ativos_correspondentes = ativos[ativos[coluna_bdativos].astype(str).str.contains(asset_name)]
        for j, ativo_linha in ativos_correspondentes.iterrows():
            if last_update_date > ativo_linha['Data Última Comunicação']:
                ativos.at[j, 'Data Última Comunicação'] = last_update_date
                print(f"{ativo_linha[coluna_bdativos]} atualizado para {last_update_date} \n")
            else:
                print(f'{ativo_linha[coluna_bdativos]} NÃO É MAIOR {last_update_date} que {ativo_linha["Data Última Comunicação"]}')
                nao_atualizados_ultima_comunicacao.append(asset_name)

    for i, linha in bases_concat.iterrows():
        asset_name = remover_separador(linha[coluna_bdconcat])
        max_sample_time_date = linha['Max Sample Time']
        ativos_correspondentes = ativos[ativos[coluna_bdativos].astype(str).str.contains(asset_name)]
        for j, ativo_linha in ativos_correspondentes.iterrows():
            if pd.isna(ativo_linha['Data Último Envio de Dados']):
                ativos.at[j, 'Data Último Envio de Dados'] = max_sample_time_date
                print(f"{ativo_linha[coluna_bdativos]} atualizado (vazio) para {max_sample_time_date} \n")
            elif max_sample_time_date > ativo_linha['Data Último Envio de Dados']:
                ativos.at[j, 'Data Último Envio de Dados'] = max_sample_time_date
                print(f"{ativo_linha[coluna_bdativos]} atualizado para {max_sample_time_date} \n")
            else:
                print(f'{ativo_linha[coluna_bdativos]} NÃO É MAIOR {max_sample_time_date} que {ativo_linha["Data Último Envio de Dados"]}')
                nao_atualizados_ultimo_envio.append(asset_name)

    print(ativos[['NºSÉRIE', 'Data Última Comunicação', 'Data Último Envio de Dados']])
    print("\n\nAssets não atualizados para Data Última Comunicação:")
    print(nao_atualizados_ultima_comunicacao)
    print("\n\nAssets não atualizados para Data Último Envio de Dados:")
    print(nao_atualizados_ultimo_envio)
    print(lista_nao_contem)
    
    caminho_saida = caminho_ativosatt
    ativos.to_excel(caminho_saida, index=False)
    print(f"\n\nTabela atualizada salva em {caminho_saida}")

    return caminho_saida, ativos, nao_atualizados_ultima_comunicacao
