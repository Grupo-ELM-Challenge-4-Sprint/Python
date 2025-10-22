import requests

# =============================================================================
# FUNÇÃO PARA ENCONTRAR FARMÁCIAS PRÓXIMAS
# =============================================================================

def encontrar_farmacias_proximas():
    print("\n╔══════════════════════════════════════════════╗")
    print("║        ENCONTRAR FARMÁCIAS PRÓXIMAS          ║")
    print("╚══════════════════════════════════════════════╝")

    api_key = "AIzaSyA6Sxw5Iyu-bPS_0brvZOWqX2X866JNcT8"

    while True:
        cep = input("\nDigite seu CEP (apenas números): ")

        if not (cep.isdigit() and len(cep) == 8):
            print("CEP inválido. Por favor, tente novamente.")
            continue

        # API de Geocoding para converter o CEP em coordenadas (latitude e longitude)
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={api_key}"

        try:
            response_geocode = requests.get(geocode_url)
            if response_geocode.status_code != 200:
                print("Erro ao obter coordenadas para o CEP. Tente novamente.")
                continue

            dados_geocode = response_geocode.json()
            if not dados_geocode.get("results"):
                print("Não foi possível encontrar a localização para este CEP. Tente novamente.")
                continue

            location = dados_geocode["results"][0]["geometry"]["location"]
            lat, lng = location["lat"], location["lng"]

            # API Places (Nearby Search) para encontrar farmácias perto dessas coordenadas
            places_url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                          f"?location={lat},{lng}"
                          f"&radius=2000"
                          f"&type=pharmacy"
                          f"&keyword=farmacia"
                          f"&language=pt-BR"
                          f"&key={api_key}")

            response_places = requests.get(places_url)
            if response_places.status_code != 200:
                print("Erro ao buscar farmácias. Tente novamente.")
                continue

            dados_places = response_places.json()
            farmacias = dados_places.get("results", [])

            if not farmacias:
                print("\nNenhuma farmácia encontrada em um raio de 2km para este CEP. Tente novamente.")
                continue

            print(f"\nFarmácias encontradas perto de você (as 5 mais próximas):\n")
            for i, farmacia in enumerate(farmacias[:5], 1):
                nome = farmacia.get("name", "Nome não disponível")
                endereco = farmacia.get("vicinity", "Endereço não disponível")
                rating = farmacia.get("rating", "Sem avaliação")
                print(f"{i}. {nome}")
                print(f"   Endereço: {endereco}")
                print(f"   Avaliação: {rating} ")
                print("-" * 40)
            break
            
        except requests.RequestException as e:
            print(f"\n❌ Erro de conexão ao consultar a API: {e}. Tente novamente.")
            continue
