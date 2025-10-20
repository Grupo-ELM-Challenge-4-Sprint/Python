from core.guia_interativo_e_ia import *
from core.crud import *
from core.tutoriais import *
from main import __name__


# =============================================================================
# FUNÇÃO COM MENU CADASTRO/LOGIN/ESQUECI SENHA
# =============================================================================

# Menu Principal do sistema
def mostrar_menu_principal():
    print("\n" + "=" * 42)
    print("         BEM-VINDO AO SIMPLESHC      ")
    print("=" * 42)
    print("1. Cadastro")
    print("2. Login")
    print("3. Recuperar Senha")
    print("4. Ajuda e Informações Gerais")
    print("0. Sair do Sistema")
    print("=" * 42)

    escolha = input("Escolha uma opção: ")

    return escolha


# =============================================================================
# FUNÇÃO PRINCIPAL DO MENU DO USUÁRIO
# =============================================================================

modo_guia_interativo_ativo = False

# Função para exibir o menu do usuário após login
# Menu Usuário
def menu_usuario_logado(usuario_logado):
    global modo_guia_interativo_ativo
    nome_usuario = usuario_logado["nome"]
    email_usuario = usuario_logado["email"]

    while True:
        print("\n╔══════════════════════════════════════════════╗")
        print(f"║  MENU DO USUÁRIO: {nome_usuario[:20]:<26} ║")
        if modo_guia_interativo_ativo:
            print("║       ⭐ Modo Guia Interativo ATIVO ⭐       ║")
        print("╚══════════════════════════════════════════════╝\n")
        
        print("1. Tutorial de como cadastrar no App HC")
        print("2. Tutorial de como logar no App HC")
        print("3. Tutorial Esqueci minha Senha no App HC")
        print("4. Tutorial de como acessar Resultados de Exames")
        print("5. Tutorial de como acessar Receitas Médicas")
        print("6. Tutorial de como acessar Minhas Agendas (Consultas/Exames)")
        print("7. Tutorial de como acessar as Teleconsulta")
        print("8. Tutorial de como acessar Solicitação de Exames")
        print("9. Tutorial de como acessar Solicitação de Documentos")
        print("10. Tutorial de como acessar os Meus Dados")
        print("11. IA e Guia Interativo")
        if verificar_se_eh_admin(usuario_logado):
            print("12. Acesso Administrativo")
        print("0. Sair (Logout)")
        print("=" * 46)

        opcao_login = input("Digite o número da opção desejada e pressione Enter: ")

        # Cada bloco abaixo trata uma opção do menu do usuário
        match opcao_login:
            case '1':  # Tutorial de Cadastro
                tutorial_cadastro(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")
            
            case '2':  # Tutorial de Login
                tutorial_login(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '3':  # Tutorial Esqueci Senha
                tutorial_esqueci_senha(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '4':  # Tutorial de Resultados
                tutorial_resultados(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '5':  # Tutorial de Receitas
                tutorial_receitas(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '6':  # Tutorial de Agendas
                tutorial_agendas(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '7':  # Tutorial de Teleconsulta
                tutorial_teleconsulta(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '8':  # Solicitação de Exames (HC)
                tutorial_solicitacao_exames(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '9':  # Solicitação de Documentos (HC)
                tutorial_solicitacao_documentos(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '10':  # Meus Dados
                tutorial_meus_dados(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '11':  # IA e Guia Interativo
                modo_guia_interativo_ativo = guia_interativo_e_ia(modo_guia_interativo_ativo)

            case '12':  # Acesso Administrativo
                if verificar_se_eh_admin(usuario_logado):
                    menu_administrativo(usuario_logado)
                else:
                    print("\n❌ Acesso negado! Você não tem permissão de administrador.")
                    input("Pressione Enter para continuar...")

            case '0':
                print(f"\nSaindo do seu usuário... Até logo, {nome_usuario}!")
                break
            
            case _:
                print("\nOpção inválida. Por favor, escolha uma opção válida do menu.")
                if modo_guia_interativo_ativo:
                    print("[Guia]: Certifique-se de digitar apenas o número da opção desejada (ex: 1, 2, 3...).")
