from fastapi import FastAPI
import httpx
from typing import Optional
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

KONNEKTIVE_API_URL = "https://api.konnektive.com"

class PageType(Enum):
    lead = "leadPage"
    order = "orderPage"
    upsell = "upsellPage"
    thankYou = "thankYouPage"

class click_params(BaseModel):
    pageType: PageType
    sessionId: Optional[str]
    campaignId: Optional[str]

# GET /products
# POST /clicks
# POST /leads
# POST /orders
#  - pre auth
#  - verify data
#  - calc sales tax & shipping
#  - order 
#  - if order success -> [return sucess & route upsell] || [rerun order] || [cancel order]

username = "wsapi"
password = ""

@app.post("/clicks")
async def update_clicks(params: click_params):
    async with httpx.AsyncClient() as client:
        if(params.pageType == PageType.lead.value):
            response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/?loginId={username}&password={password}&pageType=leadPage&campaignId={params.campaignId}")
        else:
            response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/?loginId={username}&password={password}&pageType={params.pageType}&sessionId={params.sessionId}")
        return response.json()

@app.get('/products')
async def get_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KONNEKTIVE_API_URL}/product/query/?loginId={username}&password={password}")
        return response.json()