import requests, json

def get_last_pokemon(evolves_to, no_evolution_pokemon, less_weight_name, less_weight):
    # GET LAST POKEMON FROM EVOLUTION TREE
    for item in evolves_to:
        if item['evolves_to'] == []:
            pokemon_name = item['species']['name']

            # ----------------- GET WEIGHT -----------------
            url = "https://pokeapi.co/api/v2/pokemon/"
            response = requests.get(url+pokemon_name)

            if response.status_code == 404:
                url_species = item['species']['url']

                response = requests.get(url_species)

                id = response.json()['id']
                response = requests.get(url+str(id))

            data = response.json()

            pokemon_weight = data["weight"]

            # ----------------- COMPARE WEIGHT -----------------
            if less_weight > pokemon_weight:
                less_weight = pokemon_weight
                less_weight_name = pokemon_name

            no_evolution_pokemon.append(pokemon_name)
        else:
            get_last_pokemon(item['evolves_to'], no_evolution_pokemon, less_weight_name, less_weight)

    return no_evolution_pokemon, less_weight_name, less_weight

def tree_evolution(data, no_evolution_pokemon, less_weight_name, less_weight):
    chain = data['chain']
    evolves_to = chain['evolves_to']
    if evolves_to == []:
        pokemon_name = chain['species']['name']
        
        # ----------------- GET WEIGHT -----------------
        url = "https://pokeapi.co/api/v2/pokemon/"
        response = requests.get(url+pokemon_name)
        
        if response.status_code == 404:
            url_species = chain['species']['url']

            response = requests.get(url_species)

            id = response.json()['id']
            response = requests.get(url+str(id))
        
        data = response.json()

        pokemon_weight = data["weight"]
        # ----------------- COMPARE WEIGHT -----------------
        if less_weight > pokemon_weight:
            less_weight = pokemon_weight
            less_weight_name = pokemon_name

        no_evolution_pokemon.append(pokemon_name)

        return no_evolution_pokemon, less_weight_name, less_weight

    no_evolution_pokemon, less_weight_name, less_weight = get_last_pokemon(evolves_to, no_evolution_pokemon, less_weight_name, less_weight)
    return no_evolution_pokemon, less_weight_name, less_weight
    
# PRINCIPAL FUNCTION
def get_no_evolution_pokemon():
    # URL DEFINITION
    url_evolution = "https://pokeapi.co/api/v2/evolution-chain/?limit=50"

    # SOLUTION VARIABLES
    no_evolution_pokemon = []
    less_weight_name = ""
    less_weight = 1000

    next = True

    # SEE ALL THE PAGES
    while(next):
        response = requests.get(url_evolution)

        # EXTRACT DATA
        data = response.json()

        url_evolution = data['next']
        next = url_evolution != None

        for url in data['results']:
            response = requests.get(url['url'])
            data = response.json()

            no_evolution_pokemon, less_weight_name, less_weight = tree_evolution(data, no_evolution_pokemon, less_weight_name, less_weight)

    solution = {
        "no_evolution_pokemon": no_evolution_pokemon,
        "less_weight_pokemon": {
            "name": less_weight_name,
            "weight": less_weight
        }
    }

    with open('solution.json', 'w') as file:
        json.dump(solution, file, indent=4)

get_no_evolution_pokemon()