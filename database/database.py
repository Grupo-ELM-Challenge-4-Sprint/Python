# =============================================================================
# MÓDULO DE CONEXÃO E OPERAÇÕES COM BANCO DE DADOS
# =============================================================================

import oracledb
import json

SERVIDOR = 'oracle.fiap.com.br'
PORTA = 1521
SERVICO = 'ORCL'

def abre_conexao():
    usuario = 'rm561432'  # input('username: ')
    senha = '301006'  # getpass('senha: ')

    try:
        conexao = oracledb.connect(
            user=usuario,
            password=senha,
            dsn=f'{SERVIDOR}:{PORTA}/{SERVICO}'
        )
        print('Conexão com o Banco de Dados estabelecida.')
        return conexao
    except oracledb.Error as e:
        print(f'Erro ao conectar ao banco de dados: {e}')
        return None

def fecha_conexao(conexao, cursor=None):
    if cursor:
        try:
            cursor.close()
        except oracledb.InterfaceError:
            pass
    if conexao:
        conexao.close()
        print('Conexão com o Banco de Dados fechada.')

def existe_tabela(cursor, nome_tabela):
    query = 'SELECT table_name FROM user_tables WHERE table_name = :nome'
    cursor.execute(query, {'nome': nome_tabela.upper()})
    resultados = cursor.fetchall()
    return len(resultados) == 1


def coluna_existe(cursor, tabela, coluna):
    query = 'SELECT column_name FROM user_tab_columns WHERE table_name = :tabela AND column_name = :coluna'
    cursor.execute(query, {'tabela': tabela.upper(), 'coluna': coluna.upper()})
    return cursor.fetchone() is not None


def cria_tabelas_se_nao_existirem(cursor, conexao):
    query_usuarios = '''
    CREATE TABLE USUARIOS (
        cpf VARCHAR(11) PRIMARY KEY,
        nome VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        celular VARCHAR(15),
        senha VARCHAR(100)
    )
    '''
    try:
        cursor.execute(query_usuarios)
        conexao.commit()
    except oracledb.DatabaseError as e:
        if 'ORA-00955' in str(e) or 'already exists' in str(e).lower():
            pass
        else:
            raise

    # Tabela de Consultas
    query_consultas = '''
    CREATE TABLE CONSULTAS (
        id NUMBER PRIMARY KEY,
        usuario_cpf VARCHAR(11),
        data_consulta DATE,
        hora_consulta VARCHAR(5),
        especialidade VARCHAR(100),
        medico VARCHAR(100),
        local_consulta VARCHAR(200),
        status VARCHAR(20) DEFAULT 'Agendada'
    )
    '''
    try:
        cursor.execute(query_consultas)
        conexao.commit()
    except oracledb.DatabaseError as e:
        if 'ORA-00955' in str(e) or 'already exists' in str(e).lower():
            pass
        else:
            raise

    # Tabela de Receitas
    query_receitas = '''
    CREATE TABLE RECEITAS (
        id NUMBER PRIMARY KEY,
        usuario_cpf VARCHAR(11),
        medicamento VARCHAR(200),
        dosagem VARCHAR(200),
        duracao VARCHAR(50),
        proxima_dose TIMESTAMP,
        instrucoes VARCHAR(500),
        status VARCHAR(20) DEFAULT 'Ativa'
    )
    '''
    try:
        cursor.execute(query_receitas)
        conexao.commit()
    except oracledb.DatabaseError as e:
        if 'ORA-00955' in str(e) or 'already exists' in str(e).lower():
            pass
        else:
            raise


def obter_consultas_usuario(cursor, usuario_cpf):
    query = '''
    SELECT id, data_consulta, hora_consulta, especialidade, medico, local_consulta, status
    FROM CONSULTAS
    WHERE usuario_cpf = :cpf
    ORDER BY data_consulta, hora_consulta
    '''
    cursor.execute(query, {'cpf': usuario_cpf})
    resultados = cursor.fetchall()

    consultas = []
    for res in resultados:
        consulta = {
            'id': res[0],
            'data': res[1].strftime('%Y-%m-%d'),
            'hora': res[2],
            'especialidade': res[3],
            'medico': res[4],
            'local': res[5],
            'status': res[6]
        }
        consultas.append(consulta)

    return consultas


def obter_receitas_usuario(cursor, usuario_cpf):
    query = '''
    SELECT id, medicamento, dosagem, duracao, proxima_dose, instrucoes, status
    FROM RECEITAS
    WHERE usuario_cpf = :cpf AND status = 'Ativa'
    ORDER BY proxima_dose
    '''
    cursor.execute(query, {'cpf': usuario_cpf})
    resultados = cursor.fetchall()

    receitas = []
    for res in resultados:
        receita = {
            'id': res[0],
            'medicamento': res[1],
            'dosagem': res[2],
            'duracao': res[3],
            'proxima_dose': res[4].strftime('%Y-%m-%d %H:%M') if res[4] else 'N/A',
            'instrucoes': res[5],
            'status': res[6]
        }
        receitas.append(receita)

    return receitas


def marcar_dose_tomada(cursor, conexao, receita_id, usuario_cpf):
    query = '''
    UPDATE RECEITAS
    SET proxima_dose = SYSDATE + INTERVAL '6' HOUR
    WHERE id = :id AND usuario_cpf = :cpf
    '''
    cursor.execute(query, {'id': receita_id, 'cpf': usuario_cpf})
    conexao.commit()

    if cursor.rowcount > 0:
        print(f"Dose de receita ID {receita_id} marcada como tomada!")
    else:
        print("Receita não encontrada ou erro ao atualizar.")


def inserir_consulta(cursor, conexao, usuario_cpf, data_consulta, hora_consulta, especialidade, medico, local_consulta):
    # Obter próximo ID
    cursor.execute("SELECT NVL(MAX(id), 0) + 1 FROM CONSULTAS")
    consulta_id = cursor.fetchone()[0]

    query = '''
    INSERT INTO CONSULTAS (id, usuario_cpf, data_consulta, hora_consulta, especialidade, medico, local_consulta)
    VALUES (:id, :cpf, TO_DATE(:data, 'YYYY-MM-DD'), :hora, :especialidade, :medico, :local)
    '''
    cursor.execute(query, {
        'id': consulta_id,
        'cpf': usuario_cpf,
        'data': data_consulta,
        'hora': hora_consulta,
        'especialidade': especialidade,
        'medico': medico,
        'local': local_consulta
    })
    conexao.commit()
    print("Consulta inserida com sucesso!")


def inserir_receita(cursor, conexao, usuario_cpf, medicamento, dosagem, duracao, proxima_dose, instrucoes):
    # Obter próximo ID
    cursor.execute("SELECT NVL(MAX(id), 0) + 1 FROM RECEITAS")
    receita_id = cursor.fetchone()[0]

    query = '''
    INSERT INTO RECEITAS (id, usuario_cpf, medicamento, dosagem, duracao, proxima_dose, instrucoes)
    VALUES (:id, :cpf, :medicamento, :dosagem, :duracao, TO_TIMESTAMP(:proxima_dose, 'YYYY-MM-DD HH24:MI'), :instrucoes)
    '''
    cursor.execute(query, {
        'id': receita_id,
        'cpf': usuario_cpf,
        'medicamento': medicamento,
        'dosagem': dosagem,
        'duracao': duracao,
        'proxima_dose': proxima_dose,
        'instrucoes': instrucoes
    })
    conexao.commit()
    print("Receita inserida com sucesso!")


def atualizar_consulta(cursor, conexao, consulta_id, usuario_cpf, data_consulta, hora_consulta, especialidade, medico, local_consulta, status):
    query = '''
    UPDATE CONSULTAS
    SET data_consulta = TO_DATE(:data, 'YYYY-MM-DD'),
        hora_consulta = :hora,
        especialidade = :especialidade,
        medico = :medico,
        local_consulta = :local,
        status = :status
    WHERE id = :id AND usuario_cpf = :cpf
    '''
    cursor.execute(query, {
        'data': data_consulta,
        'hora': hora_consulta,
        'especialidade': especialidade,
        'medico': medico,
        'local': local_consulta,
        'status': status,
        'id': consulta_id,
        'cpf': usuario_cpf
    })
    conexao.commit()

    if cursor.rowcount > 0:
        print("Consulta atualizada com sucesso!")
    else:
        print("Consulta não encontrada ou erro ao atualizar.")


def atualizar_receita(cursor, conexao, receita_id, usuario_cpf, medicamento=None, dosagem=None, duracao=None, proxima_dose=None, instrucoes=None, status=None):
    updates = []
    params = {'id': receita_id, 'cpf': usuario_cpf}

    if medicamento:
        updates.append("medicamento = :medicamento")
        params['medicamento'] = medicamento
    if dosagem:
        updates.append("dosagem = :dosagem")
        params['dosagem'] = dosagem
    if duracao:
        updates.append("duracao = :duracao")
        params['duracao'] = duracao
    if proxima_dose:
        updates.append("proxima_dose = TO_TIMESTAMP(:proxima_dose, 'YYYY-MM-DD HH24:MI')")
        params['proxima_dose'] = proxima_dose
    if instrucoes:
        updates.append("instrucoes = :instrucoes")
        params['instrucoes'] = instrucoes
    if status:
        updates.append("status = :status")
        params['status'] = status

    if not updates:
        print("Nenhum campo para atualizar.")
        return

    query = f'''
    UPDATE RECEITAS
    SET {', '.join(updates)}
    WHERE id = :id AND usuario_cpf = :cpf
    '''
    cursor.execute(query, params)
    conexao.commit()

    if cursor.rowcount > 0:
        print("Receita atualizada com sucesso!")
    else:
        print("Receita não encontrada ou erro ao atualizar.")


def remover_consulta(cursor, conexao, consulta_id, usuario_cpf):
    query = '''
    DELETE FROM CONSULTAS
    WHERE id = :id AND usuario_cpf = :cpf
    '''
    cursor.execute(query, {'id': consulta_id, 'cpf': usuario_cpf})
    conexao.commit()

    if cursor.rowcount > 0:
        print("Consulta removida com sucesso!")
    else:
        print("Consulta não encontrada ou erro ao remover.")

def remover_receita(cursor, conexao, receita_id, usuario_cpf):
    query = '''
    DELETE FROM RECEITAS
    WHERE id = :id AND usuario_cpf = :cpf
    '''
    cursor.execute(query, {'id': receita_id, 'cpf': usuario_cpf})
    conexao.commit()

    if cursor.rowcount > 0:
        print("Receita removida com sucesso!")
    else:
        print("Receita não encontrada ou erro ao remover.")




def exportar_para_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Dados exportados para {nome_arquivo}!")


def cadastrar_usuario(cursor, conexao, cpf, nome, email, celular, senha):
    query = '''
    INSERT INTO USUARIOS (cpf, nome, email, celular, senha)
    VALUES (:cpf, :nome, :email, :celular, :senha)
    '''
    cursor.execute(query, {
        'cpf': cpf,
        'nome': nome,
        'email': email,
        'celular': celular,
        'senha': senha
    })
    conexao.commit()
    print("Usuário cadastrado com sucesso!")


def verificar_login(cursor, cpf, senha):
    query = '''
    SELECT cpf, nome, email, celular
    FROM USUARIOS
    WHERE cpf = :cpf AND senha = :senha
    '''
    cursor.execute(query, {'cpf': cpf, 'senha': senha})
    resultado = cursor.fetchone()

    if resultado:
        return {
            'cpf': resultado[0],
            'nome': resultado[1],
            'email': resultado[2],
            'celular': resultado[3]
        }
    return None