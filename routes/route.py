from datetime import datetime
from models.model import Trade
from database import collection
from typing import Optional, List
from pymongo import DESCENDING, ASCENDING
from fastapi import APIRouter, HTTPException,Query
from controllers import trades


router =APIRouter(
    prefix="/user",
    tags=['user']
)

@router.post("/trades/")
async def create_trade(trade: Trade ):
    return trades.create_trade(trade)

@router.get("/trades/", response_model=List[Trade])
async def get_all_trades(skip: int = 0, limit: int = 100):
    return trades.get_all_trades(skip,limit)

@router.get("/trades/{id}",response_model=Trade)
async def get_by_id(id:str):
    return trades.get_by_id(id)



@router.get("/tradeid/{trade_id}", response_model=Trade)
async def read_trade(trade_id: str):
    return trades.read_trade(trade_id)


@router.get("/tradesearching/", response_model=List[Trade])
async def read(skip: int = 0, limit: int = 5, search: Optional[str] = None):
   return trades.read(skip,limit,search)


@router.get("/advancefiltering/", response_model=List[Trade])
async def reading(skip: int = 0, limit: int = 5, 
                      assetClass: Optional[str] = Query(None),
                      end: Optional[datetime] = Query(None),
                      maxPrice: Optional[float] = Query(None),
                      minPrice: Optional[float] = Query(None),
                      start: Optional[datetime] = Query(None),
                      tradeType: Optional[str] = Query(None),
                      sort_by: Optional[str] = Query("tradeDetails.price", description="Name of field to sort by"),
                      sort_order: Optional[str] = Query("asc",  description="Sort order (asc or desc)")):
    return trades.reading(skip,limit,assetClass,end,maxPrice,minPrice,start,tradeType,sort_by,sort_order)