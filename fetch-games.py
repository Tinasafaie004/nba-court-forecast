import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

load_dotenv(override=True)  #reads .env file an dloads the values into environment vars

api_key=os.getenv("BALLDONTLIE_API_KEY")

if not api_key:
    raise ValueError("Missing BALLDONTLIE_API_KEY in .env")

response=requests.get(
    "https://api.balldontlie.io/v1/games", 
    params= {
        "seasons[]":2024,
        "per_page":5
    },
    headers={"Authorization":api_key},  #extra info with the request
    timeout=30
)  #server sends a JSON


print("Status:", response.status_code)
response.raise_for_status()

payload=response.json()  #turns it into a python dictionary or list
# print(type(payload))
# print(payload.keys())

games=payload["data"]
#inspecting
print(type(games))  #list
print(len(games))
print(games[0])  # a dict --> so it's a list of dictioanries 

games_df= pd.DataFrame(games)
# print("Games Columns: ",games_df.columns.to_list())
# print("First Game Record: ")
# print(games_df.iloc[0])  # I see home team and visitor team is included which is another dict

# print("Pagination: ", payload.get("meta"))

snapshot={
    "retrieved at":datetime.now(timezone.utc).isoformat(),
    "endpoint":"https://api.balldontlie.io/v1/games",
    "query_params":{"seasons[]":2024, "per_page":5},
    "response":payload

}

output_folder=Path("data/raw")
output_folder.mkdir(parents=True,exist_ok=True)

output_file=output_folder/"2024-games_response.json"

with output_file.open("w",encoding="utf-8") as file:
    json.dump(snapshot,file,indent=2)

print("first game's home team full name",games[0]["home_team"]["full_name"])
print("Home team score:",games[0]["home_team_score"])

print("first game visitor team full name",games[0]["visitor_team"]["full_name"])
print("Visitor team score:",games[0]["visitor_team_score"])