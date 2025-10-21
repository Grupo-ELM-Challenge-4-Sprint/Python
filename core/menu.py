from core.guia_interativo_e_ia import *
from core.tutoriais import *
from core.farmacias_proximas import *
from core.lembretes import *
from database.database import abre_conexao, fecha_conexao, cria_tabelas_se_nao_existirem
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
    print("3. Ajuda e Informações Gerais")
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
def menu_usuario_logado(usuario_logado, cursor, conexao):
    global modo_guia_interativo_ativo
    nome_usuario = usuario_logado["nome"]
    email_usuario = usuario_logado["email"]

    # Conexão já estabelecida no main.py

    while True:
        print("\n╔══════════════════════════════════════════════╗")
        print(f"║  MENU DO USUÁRIO: {nome_usuario[:20]:<26} ║")
        if modo_guia_interativo_ativo:
            print("║       ⭐ Modo Guia Interativo ATIVO ⭐       ║")
        print("╚══════════════════════════════════════════════╝\n")

        print("1. Acessar Tutoriais")
        print("2. Lembretes de Consultas")
        print("3. Lembretes de Receitas")
        print("4. Farmácias próximas")
        print("5. IA e Guia Interativo")
        print("0. Sair (Logout)")

        print("=" * 46)

        opcao_login = input("Digite o número da opção desejada e pressione Enter: ")

        match opcao_login:
            case '1':  # Acessar Tutoriais
                menu_tutoriais(modo_guia_interativo_ativo)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '2':  # Lembretes de Consultas
                lembretes_consultas(modo_guia_interativo_ativo, usuario_logado["cpf"], cursor, conexao)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '3':  # Lembretes de Receitas
                lembretes_receitas(modo_guia_interativo_ativo, usuario_logado["cpf"], cursor, conexao)
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '4':  # Farmácias próximas
                encontrar_farmacias_proximas()
                input("\nPressione Enter para voltar ao menu do usuário...")

            case '5':  # IA e Guia Interativo
                modo_guia_interativo_ativo = guia_interativo_e_ia(modo_guia_interativo_ativo)

            case '0':
                print(f"\nSaindo do seu usuário... Até logo, {nome_usuario}!")
                break

            case _:
                print("\nOpção inválida. Por favor, escolha uma opção válida do menu.")
                if modo_guia_interativo_ativo:
                    print("[Guia]: Certifique-se de digitar apenas o número da opção desejada (ex: 1, 2, 3...).")
