import core.validacoes as validacoes
from database.dados import _dados_de_usuarios

# Lista para armazenar os dados dos usuários
# Cada item da lista será um dicionário com os dados do usuário
lista_de_usuarios = _dados_de_usuarios

# Função para cadastrar um novo usuário no sistema
# Solicita os dados, valida e adiciona à lista
def cadastrar_usuario():
    print("\n╔════════════════════════════════╗")
    print("║    CADASTRO DE NOVO USUÁRIO    ║")
    print("╚════════════════════════════════╝\n")

    print("Digite 0 para cancelar o Cadastro\n")

    # Nome completo com validação e opção de cancelar
    while True:
        nome = input("Nome Completo: ")
        if nome == '0':
            print("Cadastro cancelado.")
            return
        if validacoes.validar_nome(nome):
            break
        print("Nome inválido. Digite ao menos 2 letras.")

    # Loop para garantir que o CPF seja válido e não duplicado
    while True:
        cpf = input("CPF (apenas 11 números): ")
        if cpf == '0':
            print("Cadastro cancelado.")
            return
        if not validacoes.validar_cpf(cpf):
            print("CPF inválido. Deve conter 11 números.")
            continue
        # Verifica se o CPF já existe na lista de usuários
        if any(usuario["cpf"] == cpf for usuario in lista_de_usuarios):
            print("Usuário com este CPF já cadastrado. Informe outro CPF.")
            continue
        break

    # Loop para garantir que o email seja válido
    #Verifica se o Email está escrito corretamente
    while True:
        email = input("Email: ")
        if email == '0':
            print("Cadastro cancelado.")
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
            return
        if not validacoes.validar_senha(senha):
            print("Senha fraca. Use ao menos 6 caracteres.")
            continue
        confirmar_senha = input("Confirme a senha: ")
        if senha == confirmar_senha:
            break
        else:
            print("As senhas não coincidem. Tente novamente.")
    
    # Cria o dicionário do novo usuário e adiciona à lista
    novo_usuario = {"cpf": cpf, "nome": nome, "email": email, "celular": celular, "senha": senha, "admin": False}
    lista_de_usuarios.append(novo_usuario)

# Função para login do usuário
# Solicita CPF e senha, verifica e retorna o usuário logado ou None
def fazer_login():
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

        usuario_encontrado = None
        for usuario in lista_de_usuarios:
            if usuario["cpf"] == cpf_login:
                usuario_encontrado = usuario
                break

        # Se não existe usuário com esse CPF, informa e faz o usuário inserir novamente o cpf
        if not usuario_encontrado:
            print("Usuário não encontrado. Verifique o CPF ou cadastre-se.")
            continue

        while True:
            senha_login = input("Senha: ")
            
            if senha_login == '0':
                print("Login cancelado.")
                return

            if usuario_encontrado["senha"] != senha_login:
                print("Senha incorreta. Tente novamente.")
                continue
            else:
                print(f"\nLogin bem-sucedido! Bem-vindo(a), {usuario_encontrado['nome']}!")
                return usuario_encontrado

# Redefinir senha do usuário
# Função para recuperar senha do SimplesHC usando CPF e email
def recuperar_senha():
    print("\n╔══════════════════════════════════════════════╗")
    print("║        REDEFINIR DE SENHA - SIMPLESHC        ║")
    print("╚══════════════════════════════════════════════╝\n")
    
    print("Digite 0 para cancelar o Cadastro\n")

    while True:
        cpf = input("Digite seu CPF (11 dígitos): ")
        if cpf == '0':
            return
        
        if not validacoes.validar_cpf(cpf):
            print("CPF inválido. Digite apenas 11 números.")
            continue
        
        # Busca o usuário pelo CPF
        usuario_encontrado = None
        for usuario in lista_de_usuarios:
            if usuario["cpf"] == cpf:
                usuario_encontrado = usuario
                break
        
        if not usuario_encontrado:
            print("Usuário não encontrado. Verifique o CPF ou cadastre-se.")
            continue
        
        # Solicita o email para confirmação
        email = input("Digite o email cadastrado: ")
        
        if usuario_encontrado["email"] != email:
            print("Email não confere com o cadastrado. Tente novamente.")
            continue
        
        print(f"\n✅ Dados confirmados!")
        print(f"Usuário: {usuario_encontrado['nome']}")
        print(f"Email: {usuario_encontrado['email']}")
        
        # Permite definir nova senha
        while True:
            nova_senha = input("\nDigite sua nova senha (mín. 6 caracteres): ")
            if not validacoes.validar_senha(nova_senha):
                print("Senha muito fraca. Use pelo menos 6 caracteres.")
                continue
            
            confirmar_senha = input("Confirme a nova senha: ")
            if nova_senha == confirmar_senha:
                usuario_encontrado['senha'] = nova_senha
                print("✅ Senha alterada com sucesso! Agora você pode fazer login.")
                break
            else:
                print("❌ Senhas não coincidem. Tente novamente.")
        
        break