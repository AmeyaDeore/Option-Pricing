from fastapi import FastAPI, HTTPException
from data_pipeline import get_options_data
from fastapi.middleware.cors import CORSMiddleware
from cachetools import TTLCache, cached

app = FastAPI(title="IV Surface API")

# Add CORS middleware just in case
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache with 5 minutes (300 seconds) TTL, max 100 items
cache = TTLCache(maxsize=100, ttl=300)

@app.get("/api/iv-surface/{ticker}")
@cached(cache)
def fetch_iv_surface(ticker: str):
    try:
        df = get_options_data(ticker)
        # Convert dataframe to a list of dictionaries for JSON response
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
