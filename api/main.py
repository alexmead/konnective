from fastapi import FastAPI
import httpx

app = FastAPI()

POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon"
KONNEKTIVE_API_URL = "https://api.konnektive.com"

# GET /products
# POST /clicks
# POST /leads
# POST /orders
#  - pre auth
#  - verify data
#  - calc sales tax & shipping
#  - order 
#  - if order success -> [return sucess & route upsell] || [rerun order] || [cancel order]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pokemon API Wrapper!"}

@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEMON_API_URL}/{name}")
        if response.status_code == 200:
            return response.json()
        return {"error": "Pokemon not found"}