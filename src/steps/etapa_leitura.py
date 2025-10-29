from excel.leitor_excel import ler_planilha

def executar_leitura():
    df = ler_planilha()
    # Aqui eu posso aplicar filtros, validações, etc.
    return df