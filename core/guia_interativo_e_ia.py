def guia_interativo_e_ia(modo_guia_interativo_ativo):
    while True:
        print("\n╔══════════════════════════════════════════════╗")
        print("║            IA e Guia Interativo              ║")
        if modo_guia_interativo_ativo:
            print("║         ⭐ Modo Guia Interativo ATIVO ⭐     ║")
        print("╚══════════════════════════════════════════════╝\n")
        print("Olá! Esta é a sua Central para gerenciar o Guia Interativo e falar com a IA do SimplesHC.")
        print("Selecione um tópico para saber mais:")
        print("1. Falar com o Assistente Virtual (para Perguntas Frequentes).")
        print(f"2. Modo Guia Interativo: [{'DESATIVAR' if modo_guia_interativo_ativo else 'ATIVAR'}] Ajuda visual passo a passo.")
        print("\n0. Voltar ao menu do usuário.")
        print("=" * 50)

        prompt_ajuda = "Escolha uma opção de ajuda (digite o número): "
        if modo_guia_interativo_ativo:
            prompt_ajuda = "[Guia] Digite o número da ajuda que precisa (1, 2 ou 0): "

        escolha_ajuda = input(prompt_ajuda)
        
        if escolha_ajuda == '1':
            print("\n--- Assistente Virtual ---")
            print("[Assistente Virtual]: Olá! Sou o assistente virtual do SimplesHC. Posso ajudar com dúvidas frequentes.")
            print("  Por exemplo, você pode perguntar:")
            print("    'Como vejo meus exames?'")
            print("    'Esqueci minha senha, e agora?'")
            print("    'Como funciona a teleconsulta?'")
            user_query = input("Digite sua pergunta (ou 'sair' para voltar): ").lower()
            
            if "exames" in user_query or "resultados" in user_query:
                print("[Assistente Virtual]: Para ver resultados, acesse a seção 'Resultados de Exames' no Portal do Paciente HC após o login.")
            elif "senha" in user_query:
                print("[Assistente Virtual]: Se esqueceu sua senha, na tela de login principal, deveria haver uma opção 'Esqueci minha senha'.")
            elif "teleconsulta" in user_query:
                print("[Assistente Virtual]: Para teleconsultas, confirme data e horário em 'Agendas' e acesse o link no horário marcado.")
            elif user_query == 'sair':
                print("[Assistente Virtual]: Entendido! Se precisar de mais algo, é só chamar.")
            else:
                print("[Assistente Virtual]: Desculpe, ainda estou aprendendo. Para essa dúvida, sugiro consultar as outras opções de ajuda ou contatar o suporte humano do hospital.")
        
        elif escolha_ajuda == '2':
            modo_guia_interativo_ativo = not modo_guia_interativo_ativo
            if modo_guia_interativo_ativo:
                print("\n⭐ Modo Guia Interativo ATIVADO! ⭐")
                print("   A partir de agora, você verá mais dicas e explicações ([Guia]: ...) ao usar o sistema.")
                print("   Isso pode ajudar a entender melhor cada passo.")
            else:
                print("\nModo Guia Interativo DESATIVADO.")
                print("   As dicas extras ([Guia]: ...) não serão mais exibidas.")
            print("Você pode ativar ou desativar este modo quando quiser.")
        elif escolha_ajuda == '0':
            return modo_guia_interativo_ativo
        else:
            print("Opção de ajuda inválida. Por favor, escolha um número válido do menu.")
        input("\nPressione Enter para continuar na Ajuda ou '0' para voltar ao menu do usuário...")