import os
from datetime import datetime, timezone
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

class ClickParams(BaseModel):
    pageType: str
    campaignId: Optional[str] = Field(default=None)
    sessionId: Optional[str] = Field(default=None)
    requestUri: Optional[str] = Field(default=None)

class LeadParams(BaseModel):
    campaignId: str
    orderId: str
    payerId: str
    paypalBillerId: str
    product1_id: str
    sessionId: str
    token: str

class OrderParams(BaseModel):
    firstName: str
    lastName: str
    address1: str
    address2: Optional[str] = Field(default=None)
    postalCode: str
    city: str
    state: str
    country: str
    altFirstName: Optional[str] = Field(default=None)
    altLastName: Optional[str] = Field(default=None)
    altAddress1: Optional[str] = Field(default=None)
    altAddress2: Optional[str] = Field(default=None)
    altPostalCode: Optional[str] = Field(default=None)
    altCity: Optional[str] = Field(default=None)
    altState: Optional[str] = Field(default=None)
    altCountry: Optional[str] = Field(default=None)
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
            "firstName": params.altFirstName if params.altFirstName else params.firstName,
            "lastName": params.altLastName if params.altLastName else params.lastName,
            "address1": params.altAddress1 if params.altAddress1 else params.address1,
            "postalCode": params.altPostalCode if params.altPostalCode else params.postalCode,
            "city": params.altCity if params.altCity else params.city,
            "state": params.altState if params.altState else params.state,
            "country": params.altCountry if params.altCountry else params.country,
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
        }
        if params.altAddress2:
            query_params["address2"] = params.altAddress2
            query_params["shipAddress2"] = params.address2
        else: 
            query_params["address2"] = params.address2
            query_params["shipAddress2"] = params.address2

        response = await client.post(f"{KONNEKTIVE_API_URL}/order/import/", params=query_params)
        return response.json()

@app.post("/click")
async def update_clicks(params: ClickParams):
    async with httpx.AsyncClient() as client:
        query_params = {
            "loginId": username,
            "password": password,
            "pageType": params.pageType.value,
            "sessionId": params.sessionId,
            "requestUri": params.requestUri,
            "campaignId": params.campaignId
        }
        if(params.pageType.value == PageType.lead.value):
            query_params.pop("sessionId")
            response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/", params=query_params)
        else:
            query_params.pop("campaignId")
            query_params.pop("requestUri")
            response = await client.post(f"{KONNEKTIVE_API_URL}/landers/clicks/import/", params=query_params)
        return response.json()

@app.post("/lead")
async def update_lead(params: LeadParams):
    async with httpx.AsyncClient() as client:
        query_params = {
            "loginId": username,
            "password": password,
            "campaignId": params.campaignId,
            "orderId": params.orderId,
            "payerId": params.payerId,
            "paypalBillerId": params.paypalBillerId,
            "product1_id": params.product1_id,
            "sessionId": params.sessionId,
            "token": params.token
        }
        response = await client.post(f"{KONNEKTIVE_API_URL}/lead/import/", params=query_params)
        return response.json()

@app.get("/product/{productId}")
async def get_product(productId: str):
        async with httpx.AsyncClient() as client:
            query_params = {
                "loginId": username,
                "password": password,
                "productId": productId
            }
            response = await client.get(f"{KONNEKTIVE_API_URL}/product/query/", params=query_params)
            return response.json()

@app.get("/products")
async def get_products():
    async with httpx.AsyncClient() as client:
        query_params = {
            "loginId": username,
            "password": password
        }
        response = await client.get(f"{KONNEKTIVE_API_URL}/product/query/", params=query_params)
        return response.json()

@app.get("/health")
async def get_health():
    return {
        "status": "ok",
        "service": "Konnektive Wrapper API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }