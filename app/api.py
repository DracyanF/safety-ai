from fastapi import FastAPI, Query
from typing import Optional

from app.search import search_similar_crimes
from app.hotspots import detect_hotspots
from app.trends import detect_trends
from app.risk import compute_risk_scores
from app.patrol import recommend_patrols
from app.explain import explain_patrol_recommendation

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Public Safety Intelligence API",
    description="AI-powered crime analysis and patrol recommendation system",
    version="1.0"
)
app.state.limiter = limiter

@app.get("/")
def root():
    return {"message": "Public Safety Intelligence API is running"}

# 🔍 SEARCH
@app.get("/search")
def search(
    query: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: Optional[float] = None,
    days: Optional[int] = None,
):
    results = search_similar_crimes(
        query=query,
        lat=lat,
        lon=lon,
        radius_km=radius_km,
        days=days
    )

    return [p.payload for p in results]

# 🔥 HOTSPOTS
@app.get("/hotspots")
def hotspots(
    days: int = Query(30),
    threshold: int = Query(3)
):
    return detect_hotspots(days=days, threshold=threshold)

# 📈 TRENDS
@app.get("/trends")
def trends(
    window_days: int = Query(15)
):
    return detect_trends(window_days=window_days)

# 🚦 RISK SCORES
@app.get("/risk")
def risk(
    days: int = Query(30)
):
    return compute_risk_scores(days=days)

# 🚓 PATROL RECOMMENDATIONS (WITH EXPLANATION)
@app.get("/patrols")
def patrols(
    days: int = Query(30)
):
    recs = recommend_patrols(days=days)

    for r in recs:
        r["explanation"] = explain_patrol_recommendation(r)

    return recs

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

@app.get("/search")
@limiter.limit("10/minute")
def search(
    request: Request,
    query: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: Optional[float] = None,
    days: Optional[int] = None,
):
    results = search_similar_crimes(
        query=query,
        lat=lat,
        lon=lon,
        radius_km=radius_km,
        days=days
    )
    return [p.payload for p in results]
