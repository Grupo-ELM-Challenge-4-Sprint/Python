import core.validacoes as validacoes
import database.database as db
from database.database import abre_conexao, fecha_conexao, verificar_login

# Função para cadastrar um novo usuário no sistema
# Solicita os dados, valida e adiciona à lista
def cadastrar_usuario(cursor, conexao):
    print("\n╔════════════════════════════════╗")
    print("║    CADASTRO DE NOVO USUÁRIO    ║")
    print("╚════════════════════════════════╝\n")

    print("Digite 0 para cancelar o Cadastro\n")

    # Nome completo com validação e opção de cancelar
    while True:
        nome = input("Nome Completo: ")
        if nome == '0':
            print("Cadastro cancelado.")
            fecha_conexao(conexao, cursor)
            return
        if validacoes.validar_nome(nome):
            break
        print("Nome inválido. Digite ao menos 2 letras.")

    # Loop para garantir que o CPF seja válido e não duplicado
    while True:
        cpf = input("CPF (apenas 11 números): ")
        if cpf == '0':
            print("Cadastro cancelado.")
            fecha_conexao(conexao, cursor)
            return
        if not validacoes.validar_cpf(cpf):
            print("CPF inválido. Deve conter 11 números.")
            continue
        # Verifica se o CPF já existe no banco de dados
        cursor.execute("SELECT cpf FROM USUARIOS WHERE cpf = :cpf", {'cpf': cpf})
        if cursor.fetchone():
            print("Usuário com este CPF já cadastrado. Informe outro CPF.")
            continue
        break

    # Loop para garantir que o email seja válido
    #Verifica se o Email está escrito corretamente
    while True:
        email = input("Email: ")
        if email == '0':
            print("Cadastro cancelado.")
            fecha_conexao(conexao, cursor)
            return
        if validacoes.validar_email(email):
            break
        else:
            print("Email inválido. Formato esperado: nome@dominio.com")

    # Loop para garantir que o celular seja válido
    while True:
        celular = input("Número de Celular (com DDD, apenas números): ")
        if celular == '0':
            print("Cadastro cancelado.")
            fecha_conexao(conexao, cursor)
            return
        if validacoes.validar_celular(celular):
            break
        else:
            print("Número de celular inválido. Deve conter 10 ou 11 números.")

    # Loop para garantir que as senhas coincidam
    while True:
        senha = input("Crie uma senha (mín. 6 caracteres): ")
        if senha == '0':
            print("Cadastro cancelado.")
            fecha_conexao(conexao, cursor)
            return
        if not validacoes.validar_senha(senha):
            print("Senha fraca. Use ao menos 6 caracteres.")
            continue
        confirmar_senha = input("Confirme a senha: ")
        if senha == confirmar_senha:
            break
        else:
            print("As senhas não coincidem. Tente novamente.")

    # Cadastra o usuário no banco de dados
    db.cadastrar_usuario(cursor, conexao, cpf, nome, email, celular, senha)

# Função para login do usuário
# Solicita CPF e senha, verifica e retorna o usuário logado ou None
def fazer_login(cursor, conexao):
    print("\n╔════════════════════════════════╗")
    print("║          LOGIN USUÁRIO         ║")
    print("╚════════════════════════════════╝\n")

    print("Digite 0 para cancelar o Login\n")

    while True:
        cpf_login = input("CPF (11 dígitos): ")
        if cpf_login == '0':
            print("Login cancelado.")
            return
        if not validacoes.validar_cpf(cpf_login):
            print("CPF inválido. Digite apenas 11 números.")
            continue

        senha_login = input("Senha: ")
        if senha_login == '0':
            print("Login cancelado.")
            return

        # Verifica login no banco de dados
        usuario_encontrado = verificar_login(cursor, cpf_login, senha_login)
        if usuario_encontrado:
            print(f"\nLogin bem-sucedido! Bem-vindo(a), {usuario_encontrado['nome']}!")
            return usuario_encontrado
        else:
            print("CPF ou senha incorretos. Tente novamente.")
