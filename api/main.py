import os
from enum import Enum
from typing import Optional

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KONNEKTIVE_API_URL = "https://api.konnektive.com"

class PageType(Enum):
    lead = "leadPage"
    checkout = "checkoutPage"
    upsell = "upsellPage"
    thankYou = "thankYouPage"

class ClickParams(BaseModel):
    pageType: PageType
    sessionId: Optional[str] = Field(default=None)
    requestUri: Optional[str] = Field(default=None)
    campaignId: Optional[str] = Field(default=None)

class OrderParams(BaseModel):
    firstName: str
    lastName: str
    address1: str
    address2: Optional[str]
    postalCode: str
    city: str
    state: str
    country: str
    emailAddress: str
    phoneNumber: str
    paySource: str
    cardNumber: str
    cardMonth: str
    cardYear: str
    cardSecurityCode: str
    campaignId: str
    product1_id: str
    product1_qty: str

username = "wsapi"
password = os.getenv("KONNEKTIVE_PASSWORD")

@app.post("/order_v1")
async def update_order(params: OrderParams):
    async with httpx.AsyncClient() as client:
        query_params = {
            "loginId": username,
            "password": password,
            "firstName": params.firstName,
            "lastName": params.lastName,
            "address1": params.address1,
            "postalCode": params.postalCode,
            "city": params.city,
            "state": params.state,
            "country": params.country,
            "emailAddress": params.emailAddress,
            "phoneNumber": params.phoneNumber,
            "shipFirstName": params.firstName,
            "shipLastName": params.lastName,
            "shipAddress1": params.address1,
            "shipPostalCode": params.postalCode,
            "shipCity": params.city,
            "shipState": params.state,
            "shipCountry": params.country,
            "paySource": params.paySource,
            "cardNumber": params.cardNumber,
            "cardMonth": params.cardMonth,
            "cardYear": params.cardYear,
            "cardSecurityCode": params.cardSecurityCode,
            "campaignId": params.campaignId,
            "product1_id": params.product1_id,
            "product1_qty": params.product1_qty,
        }
        if params.address2:
            query_params["address2"] = params.address2
            query_params["shipAddress2"] = params.address2

        response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/", params=query_params)
        return response.json()

@app.post("/click/")
async def update_clicks(params: ClickParams):
    async with httpx.AsyncClient() as client:
        if(params.pageType.value == PageType.lead.value):
            response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/?loginId={username}&password={password}&pageType=leadPage&campaignId={params.campaignId}&requestUri={params.requestUri}")
        else:
            response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/?loginId={username}&password={password}&pageType={params.pageType.value}&sessionId={params.sessionId}")
        return response.json()

@app.get('/products')
async def get_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KONNEKTIVE_API_URL}/product/query/?loginId={username}&password={password}")
        return response.json()