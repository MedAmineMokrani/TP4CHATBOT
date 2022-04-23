from typing import Optional
from fastapi import FastAPI
from shodan import Shodan

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/ip/{ip}")
async def get_ip(ip: str, key: Optional[str] = None):
    if key is None:
        return {"Error": "Please provide a valid API key"}
    else:
        try:
            api = Shodan(key)
            res = api.host(ip)
            return {
                "IP": res["ip_str"],
                "Organization": res["org"],
                "Country": res["country_name"],
                "Latitude": res["latitude"],
                "Longitude": res["longitude"],
            }
            
        except Exception as e:
            return {"Error": str(e)}