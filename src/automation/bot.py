from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

def iniciar_bot(dados):
    try:
        # Configurações do Edge
        options = Options()
        options.use_chromium = True

        # ✅ Adiciona o perfil com a extensão Web PKI instalada
        options.add_argument("user-data-dir=C:\\Users\\alefd\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default")

        time.sleep(2)
        # Caminho para o driver
        servico = Service("webdriver/edgedriver_win64/msedgedriver.exe")
        navegador = webdriver.Edge(service=servico, options=options)
        pagina = navegador

        # Acessa o site da prefeitura
        pagina.get("https://bhissdigital.pbh.gov.br/nfse/")
        print("[INFO] Página acessada com sucesso.")
        time.sleep(2)

        # Clica no link de login
        link_login = pagina.find_element(By.CSS_SELECTOR, 'a[href="/nfse/pages/security/login.jsf"]')
        link_login.click()
        time.sleep(3)

        # Verifica se os campos de login estão presentes
        campos_usuario = pagina.find_elements(By.ID, "username")
        campos_senha = pagina.find_elements(By.ID, "password")

        if campos_usuario and campos_senha:
            print("[INFO] Tela de login detectada. Preenchendo credenciais...")
            campos_usuario[0].send_keys(dados["Usuario"])
            campos_senha[0].send_keys(dados["Senha"])

            botao_login = pagina.find_element(By.CSS_SELECTOR, "button.default-btn")
            botao_login.click()
            print("[SUCESSO] Login realizado com sucesso.")
        else:
            print("[INFO] Login já ativo. Pulando etapa de autenticação.")

        time.sleep(2)

        # Clica no botão "Selecionar Estabelecimento"
        pagina.find_element(By.ID, "menu:bt_select_empresa").click()
        print("[INFO] Botão 'Selecionar Estabelecimento' clicado.")
        time.sleep(0.5)

        # Aguarda tabela aparecer
        pagina.find_element(By.TAG_NAME, "table")
        time.sleep(0.5)

        # Busca CNPJ com paginação
        cnpj_alvo = dados["CNPJ"]
        if not buscar_cnpj_com_paginacao(pagina, cnpj_alvo):
            navegador.quit()
            return

        time.sleep(0.5)

        # Clica no menu de geração
        pagina.find_element(By.CSS_SELECTOR, 'img[src*="menu_geracao.png"]').click()
        print("[INFO] Menu de geração acessado.")
        time.sleep(0.5)

        # Clica na opção de data atual
        pagina.find_element(By.XPATH, '//a[contains(text(), "Clique aqui se for a data atual")]').click()
        print("[INFO] Mês de referência definido como atual.")
        time.sleep(5)

        # Confirma data
        botao_confirmar = navegador.find_element(By.ID, "MesReferenciaModalPanelSubview:formMesReferencia:bt_confirmar_comp_subs")
        botao_confirmar.click()
        time.sleep(7)

        # FLUXO UNIFICADO CPF/CNPJ
        doc = dados["CpfCnpjTomador"].replace(".", "").replace("-", "").replace("/", "")

        if len(doc) == 14:
            # --- CNPJ ---
            pagina.find_element(By.ID, "form:tipoPessoa:1").click()
            print(f"[SUCESSO] Tipo do documento CNPJ escolhido")
            time.sleep(1)

            pagina.find_element(By.ID, "form:numDocumento").click()
            pagina.find_element(By.ID, "form:numDocumento").send_keys(dados["CpfCnpjTomador"])
            print(f"[SUCESSO] CNPJ preenchido com sucesso")
            time.sleep(0.5)

            pagina.find_element(By.ID, "form:btAutoCompleteTomador").click()
            print(f"[SUCESSO] Clicou na lupa para buscar o CNPJ")
            time.sleep(1.5)

        else:
            # --- CPF ---
            print(f"[INFO] Documento padrão CPF detectado, preenchendo manualmente...")

            pagina.find_element(By.ID, "form:numDocumento").click()
            pagina.find_element(By.ID, "form:numDocumento").send_keys(dados["CpfCnpjTomador"])
            print(f"[SUCESSO] CPF preenchido com sucesso")
            time.sleep(0.5)

            # Nome do Tomador
            pagina.find_element(By.ID, "form:dnomeRazaoSocial").click()
            pagina.find_element(By.ID, "form:dnomeRazaoSocial").send_keys(dados["NomeTomador"])
            print(f"[SUCESSO] Nome do Tomador preenchido")
            time.sleep(0.3)

            # CEP
            pagina.find_element(By.ID, "form:cep").click()
            pagina.find_element(By.ID, "form:cep").send_keys(dados["CEP"])
            print(f"[SUCESSO] CEP preenchido")
            time.sleep(0.3)

            # Endereço
            pagina.find_element(By.ID, "form:logradouro").click()
            pagina.find_element(By.ID, "form:logradouro").send_keys(dados["Logradouro"])
            print(f"[SUCESSO] Endereço preenchido")
            time.sleep(0.3)

            # Número
            pagina.find_element(By.ID, "form:numero").click()
            pagina.find_element(By.ID, "form:numero").send_keys(dados["Numero"])
            print(f"[SUCESSO] Número preenchido")
            time.sleep(0.3)

            # Bairro
            pagina.find_element(By.ID, "form:bairro").click()
            pagina.find_element(By.ID, "form:bairro").send_keys(dados["Bairro"])
            print(f"[SUCESSO] Bairro preenchido")
            time.sleep(0.3)

            print(f"[SUCESSO] Formulário preenchido com sucesso!")
            print(f"[INFO] Dados enviados para: {dados['NomeTomador']}")
            time.sleep(0.3)

            # Avança para a aba "Identificação do(s) Serviço(s)"
            pagina.find_element(By.CSS_SELECTOR, "a[href*=\"controlaAbas('aba2')\"]").click()
            print("[INFO] Aba 'Identificação do(s) Serviço(s)' selecionada")
            time.sleep(1)

            # Discriminação do Serviço
            pagina.find_element(By.ID, "form:descriminacaoServico").click()
            pagina.find_element(By.ID, "form:descriminacaoServico").send_keys(dados["DescricaoServico"])
            print(f"[SUCESSO] Discriminação do serviço preenchida: {dados['DescricaoServico']}")
            time.sleep(0.5)

    except Exception as e:
        print(f"[ERRO] Falha ao processar {dados.get('Nome', 'Desconhecido')}: {e}")

def buscar_cnpj_com_paginacao(pagina, cnpj_alvo):
    while True:
        try:
            pagina.find_element(By.TAG_NAME, "table")
            time.sleep(1)

            elemento = pagina.find_element(By.XPATH, f'//table//*[contains(text(), "{cnpj_alvo}")]')
            time.sleep(0.5)
            elemento.click()
            print(f"[INFO] Empresa selecionada: {cnpj_alvo}")
            return True
        except:
            try:
                seta_verde = pagina.find_element(By.CSS_SELECTOR, 'img[src*="bt_proximo.gif"]')
                if seta_verde.is_displayed():
                    seta_verde.click()
                    time.sleep(1)
                    pagina.find_element(By.TAG_NAME, "table")
                    time.sleep(0.1)
                    print("[INFO] Avançando para próxima página...")
                else:
                    print("[ERRO] CNPJ não encontrado após todas as páginas.")
                    return False
            except:
                print("[ERRO] Botão de próxima página não encontrado.")
                return False