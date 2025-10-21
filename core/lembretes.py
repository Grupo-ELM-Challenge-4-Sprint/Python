# =============================================================================
# FUNÇÕES PARA LEMBRETES DE CONSULTAS E RECEITAS
# =============================================================================

import datetime
from database.database import (
    fecha_conexao, obter_consultas_usuario, obter_receitas_usuario,
    marcar_dose_tomada, exportar_para_json,
    atualizar_consulta, atualizar_receita, inserir_consulta, remover_consulta,
    inserir_receita, remover_receita
)

def lembretes_consultas(modo_guia_ativo, usuario_cpf, cursor, conexao):
    """
    Exibe lembretes de consultas agendadas.
    """
    print("\n╔══════════════════════════════════════════════╗")
    print("║        LEMBRETES DE CONSULTAS                ║")
    print("╚══════════════════════════════════════════════╝")

    if not conexao or not cursor:
        print("❌ Conexão com banco de dados não estabelecida.")
        return

    try:
        while True:
            consultas = obter_consultas_usuario(cursor, usuario_cpf)

            if not consultas:
                print("\n📅 Você não tem consultas agendadas no momento.")
                if modo_guia_ativo:
                    print("[Guia]: Agende uma consulta pelo Portal do Paciente HC para receber lembretes.")

            else:
                print("\n📅 Suas próximas consultas:")
                hoje = datetime.date.today()

                for i, consulta in enumerate(consultas, 1):
                    data_consulta = datetime.datetime.strptime(consulta["data"], "%Y-%m-%d").date()
                    dias_restantes = (data_consulta - hoje).days

                    if dias_restantes < 0:
                        status = "Passada"
                    elif dias_restantes == 0:
                        status = "Hoje"
                    elif dias_restantes == 1:
                        status = "Amanhã"
                    else:
                        status = f"Em {dias_restantes} dias"

                    print(f"\n{i}. {consulta['especialidade']} - {consulta['medico']}")
                    print(f"   📅 Data: {consulta['data']} ({status}) às {consulta['hora']}")
                    print(f"   📍 Local: {consulta['local']}")
                    print(f"   📊 Status: {consulta['status']}")

                print("\n" + "=" * 50)
                print("💡 DICAS PARA SUAS CONSULTAS:")
                print("• Chegue 15 minutos antes do horário marcado")
                print("• Leve exames anteriores e documentos pessoais")
                print("• Em caso de impossibilidade, cancele com antecedência")

                if modo_guia_ativo:
                    print("\n[Guia]: Você pode configurar notificações no Portal do Paciente HC.")
                    print("[Guia]: Para reagendar ou cancelar, entre em contato com a unidade.")

            print("\nOpções:")
            print("1. Criar nova consulta")
            print("2. Atualizar consulta")
            print("3. Remover consulta")
            print("4. Exportar consultas para JSON")
            print("0. Voltar ao menu")

            opcao = input("\nDigite a opção desejada: ").strip()

            if opcao == '1':
                # Criar nova consulta
                while True:
                    data = input("Data da consulta (YYYY-MM-DD): ").strip()
                    try:
                        datetime.datetime.strptime(data, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Formato inválido. Use YYYY-MM-DD. Tente novamente.")

                while True:
                    hora = input("Hora da consulta (HH:MM): ").strip()
                    try:
                        datetime.datetime.strptime(hora, "%H:%M")
                        break
                    except ValueError:
                        print("Formato inválido. Use HH:MM. Tente novamente.")

                while True:
                    especialidade = input("Especialidade: ").strip()
                    if especialidade:
                        break
                    print("Especialidade não pode ser vazia. Tente novamente.")

                while True:
                    medico = input("Médico: ").strip()
                    if medico:
                        break
                    print("Médico não pode ser vazio. Tente novamente.")

                while True:
                    local = input("Local da consulta: ").strip()
                    if local:
                        break
                    print("Local não pode ser vazio. Tente novamente.")

                inserir_consulta(cursor, conexao, usuario_cpf, data, hora, especialidade, medico, local)
                print("Consulta criada com sucesso!")

            elif opcao == '2':
                # Atualizar consulta
                if not consultas:
                    print("Nenhuma consulta para atualizar.")
                    continue
                while True:
                    consulta_id_str = input("Digite o ID da consulta a atualizar (ou 'sair' para voltar): ").strip()
                    if consulta_id_str.lower() == 'sair':
                        break
                    try:
                        consulta_id = int(consulta_id_str)
                        if consulta_id <= 0:
                            print("ID deve ser um número positivo.")
                            continue
                        break
                    except ValueError:
                        print("ID inválido. Digite um número.")
                if consulta_id_str.lower() == 'sair':
                    continue
                while True:
                    print("Campos disponíveis para atualização:")
                    print("1. Data (YYYY-MM-DD)")
                    print("2. Hora (HH:MM)")
                    print("3. Especialidade")
                    print("4. Médico")
                    print("5. Local")
                    print("6. Status")
                    campo = input("Digite o número do campo a atualizar (ou 'todos' para atualizar tudo, '0' para voltar): ").strip().lower()
                    if campo == '0' or campo == 'sair':
                        break
                    if campo == 'todos':
                        while True:
                            data = input("Nova data (YYYY-MM-DD): ").strip()
                            try:
                                datetime.datetime.strptime(data, "%Y-%m-%d")
                                break
                            except ValueError:
                                print("Formato inválido. Use YYYY-MM-DD. Tente novamente.")

                        while True:
                            hora = input("Nova hora (HH:MM): ").strip()
                            try:
                                datetime.datetime.strptime(hora, "%H:%M")
                                break
                            except ValueError:
                                print("Formato inválido. Use HH:MM. Tente novamente.")

                        while True:
                            especialidade = input("Nova especialidade: ").strip()
                            if especialidade:
                                break
                            print("Especialidade não pode ser vazia. Tente novamente.")

                        while True:
                            medico = input("Novo médico: ").strip()
                            if medico:
                                break
                            print("Médico não pode ser vazio. Tente novamente.")

                        while True:
                            local = input("Novo local: ").strip()
                            if local:
                                break
                            print("Local não pode ser vazio. Tente novamente.")

                        status = input("Novo status: ").strip()
                        atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, data_consulta=data, hora_consulta=hora, especialidade=especialidade, medico=medico, local_consulta=local, status=status)
                        break
                    else:
                        try:
                            campo_num = int(campo)
                            if campo_num == 0:
                                break
                            elif campo_num == 1:
                                while True:
                                    data = input("Nova data (YYYY-MM-DD): ").strip()
                                    try:
                                        datetime.datetime.strptime(data, "%Y-%m-%d")
                                        break
                                    except ValueError:
                                        print("Formato inválido. Use YYYY-MM-DD. Tente novamente.")
                                atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, data_consulta=data)
                                break
                            elif campo_num == 2:
                                while True:
                                    hora = input("Nova hora (HH:MM): ").strip()
                                    try:
                                        datetime.datetime.strptime(hora, "%H:%M")
                                        break
                                    except ValueError:
                                        print("Formato inválido. Use HH:MM. Tente novamente.")
                                atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, hora_consulta=hora)
                                break
                            elif campo_num == 3:
                                while True:
                                    especialidade = input("Nova especialidade: ").strip()
                                    if especialidade:
                                        break
                                    print("Especialidade não pode ser vazia. Tente novamente.")
                                atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, especialidade=especialidade)
                                break
                            elif campo_num == 4:
                                while True:
                                    medico = input("Novo médico: ").strip()
                                    if medico:
                                        break
                                    print("Médico não pode ser vazio. Tente novamente.")
                                atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, medico=medico)
                                break
                            elif campo_num == 5:
                                while True:
                                    local = input("Novo local: ").strip()
                                    if local:
                                        break
                                    print("Local não pode ser vazio. Tente novamente.")
                                atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, local_consulta=local)
                                break
                            elif campo_num == 6:
                                status = input("Novo status: ").strip()
                                atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, status=status)
                                break
                            else:
                                print("Campo inválido. Escolha entre 1-6.")
                                continue
                        except ValueError:
                            print("Entrada inválida. Digite um número.")
                            continue
                    break

            elif opcao == '3':
                # Remover consulta
                if not consultas:
                    print("Nenhuma consulta para remover.")
                    continue
                while True:
                    consulta_id_str = input("Digite o ID da consulta a remover (ou 'sair' para voltar): ").strip()
                    if consulta_id_str.lower() == 'sair':
                        break
                    try:
                        consulta_id = int(consulta_id_str)
                        if consulta_id <= 0:
                            print("ID deve ser um número positivo.")
                            continue
                        remover_consulta(cursor, conexao, consulta_id, usuario_cpf)
                        break
                    except ValueError:
                        print("ID inválido. Digite um número.")

            elif opcao == '4':
                # Exportar
                if not consultas:
                    print("Nenhuma consulta para exportar.")
                    continue
                exportar_para_json(consultas, 'consultas_usuario.json')

            elif opcao == '0':
                break

            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"❌ Erro ao acessar dados: {e}")



def lembretes_receitas(modo_guia_ativo, usuario_cpf, cursor, conexao):
    """
    Exibe lembretes de receitas médicas.
    """
    print("\n╔══════════════════════════════════════════════╗")
    print("║        LEMBRETES DE RECEITAS                 ║")
    print("╚══════════════════════════════════════════════╝")

    if not conexao or not cursor:
        print("❌ Conexão com banco de dados não estabelecida.")
        return

    try:
        while True:
            receitas = obter_receitas_usuario(cursor, usuario_cpf)

            if not receitas:
                print("\nVocê não tem receitas ativas no momento.")
                if modo_guia_ativo:
                    print("[Guia]: Suas receitas aparecerão aqui quando prescritas pelo médico.")

            else:
                print("\nSuas receitas ativas:")
                for i, receita in enumerate(receitas, 1):
                    print(f"\n{i}. {receita['medicamento']}")
                    print(f"   💊 Dosagem: {receita['dosagem']}")
                    print(f"   ⏱️ Duração: {receita['duracao']} dias")
                    print(f"   🔔 Primeira dose: {receita['proxima_dose']}")
                    print(f"   📋 Instruções: {receita['instrucoes']}")
                print("\n" + "=" * 50)
                print("⚠️  IMPORTANTE:")
                print("• Siga exatamente as instruções do médico")
                print("• Não interrompa o tratamento sem orientação")
                print("• Em caso de efeitos colaterais, consulte seu médico")
                print("• Guarde as medicações em local seguro e fresco")

                if modo_guia_ativo:
                    print("\n[Guia]: Configure lembretes no seu celular para não esquecer as doses.")
                    print("[Guia]: Para renovar receitas, consulte seu médico assistente.")

            print("\nOpções:")
            print("1. Criar nova receita")
            print("2. Atualizar receita")
            print("3. Remover receita")
            print("4. Marcar dose como tomada")
            print("5. Exportar receitas para JSON")
            print("0. Voltar ao menu")

            opcao = input("\nDigite a opção desejada: ").strip()

            if opcao == '1':
                # Criar nova receita
                while True:
                    medicamento = input("Medicamento: ").strip()
                    if medicamento:
                        break
                    print("Medicamento não pode ser vazio. Tente novamente.")

                while True:
                    dosagem = input("Dosagem: ").strip()
                    if dosagem:
                        break
                    print("Dosagem não pode ser vazia. Tente novamente.")

                while True:
                    duracao_str = input("Duração (em dias): ").strip()
                    try:
                        duracao = int(duracao_str)
                        if duracao > 0:
                            break
                        else:
                            print("Duração deve ser um número positivo. Tente novamente.")
                    except ValueError:
                        print("Duração deve ser um número inteiro válido. Tente novamente.")

                while True:
                    proxima_dose = input("Próxima dose (YYYY-MM-DD HH:MM): ").strip()
                    try:
                        datetime.datetime.strptime(proxima_dose, "%Y-%m-%d %H:%M")
                        break
                    except ValueError:
                        print("Formato inválido. Use YYYY-MM-DD HH:MM. Tente novamente.")

                while True:
                    instrucoes = input("Instruções: ").strip()
                    if instrucoes:
                        break
                    print("Instruções não podem ser vazias. Tente novamente.")

                inserir_receita(cursor, conexao, usuario_cpf, medicamento, dosagem, str(duracao), proxima_dose, instrucoes)
                print("Receita criada com sucesso!")

            elif opcao == '2':
                # Atualizar receita
                if not receitas:
                    print("Nenhuma receita para atualizar.")
                    continue
                receita_id_str = input("Digite o ID da receita a atualizar (ou 'sair' para voltar): ").strip()
                if receita_id_str.lower() == 'sair':
                    continue
                try:
                    receita_id = int(receita_id_str)
                    if receita_id == 0:
                        continue
                    print("Campos disponíveis para atualização:")
                    print("1. Medicamento")
                    print("2. Dosagem")
                    print("3. Duração")
                    print("4. Primeira dose (YYYY-MM-DD HH:MM)")
                    print("5. Instruções")
                    print("6. Status")
                    campo = input("Digite o número do campo a atualizar (ou 'todos' para atualizar tudo, '0' para voltar): ").strip().lower()
                    if campo == '0' or campo == 'sair':
                        continue
                    if campo == 'todos':
                        while True:
                            medicamento = input("Novo medicamento: ").strip()
                            if medicamento:
                                break
                            print("Medicamento não pode ser vazio. Tente novamente.")

                        while True:
                            dosagem = input("Nova dosagem: ").strip()
                            if dosagem:
                                break
                            print("Dosagem não pode ser vazia. Tente novamente.")

                        while True:
                            duracao_str = input("Nova duração (em dias): ").strip()
                            try:
                                duracao = int(duracao_str)
                                if duracao > 0:
                                    break
                                else:
                                    print("Duração deve ser um número positivo. Tente novamente.")
                            except ValueError:
                                print("Duração deve ser um número inteiro válido. Tente novamente.")

                        while True:
                            proxima_dose = input("Nova próxima dose (YYYY-MM-DD HH:MM): ").strip()
                            try:
                                datetime.datetime.strptime(proxima_dose, "%Y-%m-%d %H:%M")
                                break
                            except ValueError:
                                print("Formato inválido. Use YYYY-MM-DD HH:MM. Tente novamente.")

                        while True:
                            instrucoes = input("Novas instruções: ").strip()
                            if instrucoes:
                                break
                            print("Instruções não podem ser vazias. Tente novamente.")

                        status = input("Novo status: ").strip()
                        atualizar_receita(cursor, conexao, receita_id, usuario_cpf, medicamento=medicamento, dosagem=dosagem, duracao=str(duracao), proxima_dose=proxima_dose, instrucoes=instrucoes, status=status)
                    else:
                        campo_num = int(campo)
                        if campo_num == 0:
                            continue
                        elif campo_num == 1:
                            while True:
                                medicamento = input("Novo medicamento: ").strip()
                                if medicamento:
                                    break
                                print("Medicamento não pode ser vazio. Tente novamente.")
                            atualizar_receita(cursor, conexao, receita_id, usuario_cpf, medicamento=medicamento)
                        elif campo_num == 2:
                            while True:
                                dosagem = input("Nova dosagem: ").strip()
                                if dosagem:
                                    break
                                print("Dosagem não pode ser vazia. Tente novamente.")
                            atualizar_receita(cursor, conexao, receita_id, usuario_cpf, dosagem=dosagem)
                        elif campo_num == 3:
                            while True:
                                duracao_str = input("Nova duração (em dias): ").strip()
                                try:
                                    duracao = int(duracao_str)
                                    if duracao > 0:
                                        break
                                    else:
                                        print("Duração deve ser um número positivo. Tente novamente.")
                                except ValueError:
                                    print("Duração deve ser um número inteiro válido. Tente novamente.")
                            atualizar_receita(cursor, conexao, receita_id, usuario_cpf, duracao=str(duracao))
                        elif campo_num == 4:
                            while True:
                                proxima_dose = input("Nova próxima dose (YYYY-MM-DD HH:MM): ").strip()
                                try:
                                    datetime.datetime.strptime(proxima_dose, "%Y-%m-%d %H:%M")
                                    break
                                except ValueError:
                                    print("Formato inválido. Use YYYY-MM-DD HH:MM. Tente novamente.")
                            atualizar_receita(cursor, conexao, receita_id, usuario_cpf, proxima_dose=proxima_dose)
                        elif campo_num == 5:
                            while True:
                                instrucoes = input("Novas instruções: ").strip()
                                if instrucoes:
                                    break
                                print("Instruções não podem ser vazias. Tente novamente.")
                            atualizar_receita(cursor, conexao, receita_id, usuario_cpf, instrucoes=instrucoes)
                        elif campo_num == 6:
                            status = input("Novo status: ")
                            atualizar_receita(cursor, conexao, receita_id, usuario_cpf, status=status)
                        else:
                            print("Campo inválido.")
                except ValueError:
                    print("ID inválido.")

            elif opcao == '3':
                # Remover receita
                if not receitas:
                    print("Nenhuma receita para remover.")
                    continue
                try:
                    receita_id = int(input("Digite o ID da receita a remover: "))
                    remover_receita(cursor, conexao, receita_id, usuario_cpf)
                except ValueError:
                    print("ID inválido.")

            elif opcao == '4':
                # Marcar dose como tomada
                if not receitas:
                    print("Nenhuma receita para marcar dose.")
                    continue
                try:
                    receita_id = int(input("Digite o ID da receita: "))
                    marcar_dose_tomada(cursor, conexao, receita_id, usuario_cpf)
                except ValueError:
                    print("ID inválido.")

            elif opcao == '5':
                # Exportar
                if not receitas:
                    print("Nenhuma receita para exportar.")
                    continue
                exportar_para_json(receitas, 'receitas_usuario.json')

            elif opcao == '0':
                break

            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"❌ Erro ao acessar dados: {e}")
