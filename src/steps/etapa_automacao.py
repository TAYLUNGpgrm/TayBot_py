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
        "DescricaoServico", "CTISS", "ItemServico",
        "NaturezaOperacao", "RegimeTributacao", "MunicipioIncidencia", "Valor"
    ]

    for _, linha in df.iterrows():
        dados = linha.to_dict()

        if all(campo in dados and pd.notna(dados[campo]) for campo in campos_obrigatorios):
            # Formatações
            dados["Usuario"] = str(dados["Usuario"]).zfill(13)
            dados["CNPJ"] = formatar_cnpj(dados["CNPJ"])  # Empresa emissora
            dados["CpfCnpjTomador"] = formatar_documento(dados["CpfCnpjTomador"])  # Cliente

            print(f"[INFO] Processando linha: {dados['NomeTomador']}")
            try:
                iniciar_bot(dados)
            except Exception as e:
                print(f"[ERRO] Falha ao processar {dados['NomeTomador']}: {e}")
            time.sleep(2)
        else:
            campos_faltando = [
                campo for campo in campos_obrigatorios
                if campo not in dados or pd.isna(dados[campo])
            ]