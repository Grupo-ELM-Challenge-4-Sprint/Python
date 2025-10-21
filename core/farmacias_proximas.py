import requests
import json

# =============================================================================
# FUNÇÃO PARA ENCONTRAR FARMÁCIAS PRÓXIMAS
# =============================================================================

def encontrar_farmacias_proximas():
    """
    Busca farmácias próximas usando a API do Google Maps com base em um CEP.
    """
    print("\n╔══════════════════════════════════════════════╗")
    print("║        ENCONTRAR FARMÁCIAS PRÓXIMAS        ║")
    print("╚══════════════════════════════════════════════╝")

    # Sua chave de API foi inserida aqui.
    api_key = "AIzaSyA6Sxw5Iyu-bPS_0brvZOWqX2X866JNcT8"

    cep = input("\nDigite seu CEP para encontrar farmácias próximas (apenas números): ")

    if not (cep.isdigit() and len(cep) == 8):
        print("CEP inválido. Por favor, tente novamente.")
        return

    # 1. Primeiro, usamos a API de Geocoding para converter o CEP em coordenadas (latitude e longitude)
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={api_key}"

    try:
        response_geocode = requests.get(geocode_url)
        if response_geocode.status_code != 200:
            print("Erro ao obter coordenadas para o CEP.")
            return

        dados_geocode = response_geocode.json()
        if not dados_geocode.get("results"):
            print("Não foi possível encontrar a localização para este CEP.")
            return

        location = dados_geocode["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]

        # 2. Agora, usamos a API Places (Nearby Search) para encontrar farmácias perto dessas coordenadas
        places_url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                      f"?location={lat},{lng}"
                      f"&radius=2000"  # Raio de busca em metros (2 km)
                      f"&type=pharmacy"
                      f"&keyword=farmacia"
                      f"&language=pt-BR"
                      f"&key={api_key}")

        response_places = requests.get(places_url)
        if response_places.status_code != 200:
            print("Erro ao buscar farmácias.")
            return

        dados_places = response_places.json()
        farmacias = dados_places.get("results", [])

        if not farmacias:
            print("\nNenhuma farmácia encontrada em um raio de 2km para este CEP.")
            return

        print(f"\n📍 Farmácias encontradas perto de você (as 5 mais próximas):\n")
        for i, farmacia in enumerate(farmacias[:5], 1): # Mostra apenas as 5 primeiras
            nome = farmacia.get("name", "Nome não disponível")
            endereco = farmacia.get("vicinity", "Endereço não disponível")
            rating = farmacia.get("rating", "Sem avaliação")
            print(f"{i}. {nome}")
            print(f"   Endereço: {endereco}")
            print(f"   Avaliação: {rating} ⭐")
            print("-" * 40)

        # Opção para exportar para JSON
        exportar = input("\nDeseja exportar a lista completa para um arquivo JSON? (s/n): ").lower()
        if exportar == 's':
            with open('farmacias_proximas.json', 'w', encoding='utf-8') as f:
                json.dump(farmacias, f, ensure_ascii=False, indent=4)
            print("\n✅ Lista de farmácias exportada com sucesso para 'farmacias_proximas.json'!")

    except requests.RequestException as e:
        print(f"\n❌ Erro de conexão ao consultar a API: {e}")
