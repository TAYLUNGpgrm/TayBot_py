from excel.leitor_excel import ler_planilha
from steps.etapa_leitura import executar_leitura
from steps.etapa_automacao import executar_bot
from config import CAMINHO_PLANILHA

def executar_fluxo_total():
    df_visualizacao = ler_planilha(CAMINHO_PLANILHA)
    df = executar_leitura()

    print("[VISUALIZAÇÃO DA PLANILHA]")
    print("[Lendo Planilha Excel]")
    print(df_visualizacao.head())

    print("[DADOS REAIS DA PLANILHA]")
    print(df.head())

    executar_bot(df)

if __name__ == "__main__":
    executar_fluxo_total()