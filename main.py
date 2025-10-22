from core.cadastro_login import *
from core.menu import *
from database.database import abre_conexao, fecha_conexao, cria_tabelas_se_nao_existirem

# Inicializar conexão e criar tabelas se necessário
conexao = abre_conexao()
cursor = None
if conexao:
    cursor = conexao.cursor()
    cria_tabelas_se_nao_existirem(cursor, conexao)

# Loop principal do sistema
# Executa o menu principal e direciona para as funções conforme a escolha do usuário
if __name__ == "__main__":
    while True:
        opcao_principal = mostrar_menu_principal()

        if opcao_principal == '1':
            cadastrar_usuario(cursor, conexao)

        elif opcao_principal == '2':
            usuario_logado = fazer_login(cursor, conexao)
            if usuario_logado:
                menu_usuario_logado(usuario_logado, cursor, conexao)

        elif opcao_principal == '3':
            mostrar_menu_ajuda_principal()

        elif opcao_principal == '0':
            print("\nSaindo do sistema... Até logo!")
            break
        else:
            print("\nOpção inválida. Por favor, escolha uma opção do menu.")
            input("\nPressione Enter para tentar novamente...")

    # Fechar conexão ao sair
    if cursor and conexao:
        fecha_conexao(conexao, cursor)
