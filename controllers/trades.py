from database import collection
from datetime import datetime
from models.model import Trade
from typing import Optional, List
from pymongo import DESCENDING, ASCENDING
from uuid import uuid4
from fastapi import APIRouter, HTTPException,Query
from bson.objectid import ObjectId


def create_trade(trade: Trade ):
    result = collection.insert_one(trade.dict(by_alias=True))
    return {"trade": "trade added"}
   

def get_all_trades(skip: int = 0, limit: int = 100):
    trades = []
    for trade in collection.find().skip(skip).limit(limit):
        trades.append(Trade(**trade))
    return trades

def get_by_id(id:str):
    trade=collection.find_one({"_id": ObjectId(id)})
    if not trade:
        return {"trade not found"}
    return Trade(**trade)
    
def read_trade(trade_id: str):
    trade = collection.find_one({"tradeId": trade_id})
    if not trade:
        return {"trade not found"}
    return Trade(**trade)

def read(skip: int = 0, limit: int = 100, search: Optional[str] = None):
    trades = []
    query = {}
    if search:
        pattern = f".*{search}.*"
        query = {
            "$or": [
                {"counterparty": {"$regex": pattern, "$options": "i"}},
                {"instrumentId": {"$regex": pattern, "$options": "i"}},
                {"instrumentName": {"$regex": pattern, "$options": "i"}},
                {"trader": {"$regex": pattern, "$options": "i"}}
            ]
        }
    for trade in collection.find(query).skip(skip).limit(limit):
        trades.append(Trade(**trade))
    return trades

def reading(skip: int = 0, limit: int = 5, 
                      assetClass: Optional[str] = Query(None),
                      end: Optional[datetime] = Query(None),
                      maxPrice: Optional[float] = Query(None),
                      minPrice: Optional[float] = Query(None),
                      start: Optional[datetime] = Query(None),
                      tradeType: Optional[str] = Query(None),
                      sort_by: Optional[str] = Query("tradeDetails.price", description1="Name of field to sort by"),
                      sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)")):
    query = {}
    
    if assetClass:
        query['assetClass'] = assetClass
    
    if end:
        query['tradeDateTime'] = {'$lte': end}
    
    if maxPrice is not None and minPrice is not None:
        query['tradeDetails.price'] = {'$gte': minPrice, '$lte': maxPrice}
    elif maxPrice is not None:
        query['tradeDetails.price'] = {'$lte': maxPrice}
    elif minPrice is not None:
        query['tradeDetails.price'] = {'$gte': minPrice}
    
    if start:
        query['tradeDateTime'] = {'$gte': start}
    
    if tradeType:
        query['tradeDetails.buySellIndicator'] = tradeType
        
    sort_dir = DESCENDING if sort_order == "desc" else ASCENDING
    
    trades = []
    for trade in collection.find(query).sort(sort_by, sort_dir).skip(skip).limit(limit):
        trades.append(Trade(**trade))
    
    return trades