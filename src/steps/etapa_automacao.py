# steps/etapa_automacao.py
# steps/etapa_automacao.py
from automation.bot import iniciar_bot
import pandas as pd
import time

def formatar_cnpj(cnpj: str) -> str:
    cnpj = str(cnpj).zfill(14)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def formatar_cpf(cpf: str) -> str:
    cpf = str(cpf).zfill(11)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_documento(doc: str) -> str:
    """Detecta se é CPF ou CNPJ e retorna formatado."""
    doc = str(doc).strip()
    if len(doc) <= 11:  # CPF
        return formatar_cpf(doc)
    else:  # CNPJ
        return formatar_cnpj(doc)

def executar_bot(df):
    # Campos obrigatórios
    campos_obrigatorios = [
        "Usuario", "Senha", "CNPJ", "CpfCnpjTomador", "NomeTomador",
        "CEP", "Logradouro", "Numero", "Bairro", "Municipio", "UF",
        "DescricaoServico", "Valor"
        # "NaturezaOperacao", "RegimeTributacao", "MunicipioIncidencia"
    ]

    for index, linha in df.iterrows(): # Inclui o índice da linha para o log
        dados = linha.to_dict()

        # Verifica se todos os campos obrigatórios estão presentes e NÃO são NaN/vazios
        if all(campo in dados and pd.notna(dados[campo]) for campo in campos_obrigatorios):
            
            # Formatações
            dados["Usuario"] = str(dados["Usuario"]).zfill(13)
            dados["CNPJ"] = formatar_cnpj(dados["CNPJ"])  # Empresa emissora
            dados["CpfCnpjTomador"] = formatar_documento(dados["CpfCnpjTomador"])  # Cliente

            print(f"[INFO] Processando linha {index}: {dados['NomeTomador']}")
            
            try:
                # CHAMA O BOT (VERSÃO SIMPLES: ABRE E FECHA O NAVEGADOR A CADA NOTA)
                iniciar_bot(dados) 
                
            except Exception as e:
                print(f"[ERRO] Falha ao processar {dados['NomeTomador']}: {e}")
            
            time.sleep(2)
        else:
            # Lógica para pular a linha (mantida para robustez)
            campos_faltando = [
                campo for campo in campos_obrigatorios
                if campo not in dados or pd.isna(dados[campo])
            ]
            
            id_cliente = str(linha.get("CpfCnpjTomador", "N/D")).strip()
            nome_cliente = str(linha.get("NomeTomador", "Linha Vazia/Incompleta")).strip()
            
            # Avisa que pulou a linha
            print(f"[AVISO] Linha {index} PULADA. Faltam dados críticos (ex: {', '.join(campos_faltando[:3])}). Cliente: {nome_cliente} (Doc: {id_cliente})")