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
    "https://api.balldontlie.io/v1/teams",  #"teams" is an end point
    headers={"Authorization":api_key},  #extra info with the request
    timeout=30
)  #server sends a JSON


print("Status:", response.status_code)
response.raise_for_status()

payload=response.json()  #turns it into a python dictionary or list
# print(type(payload))
# print(payload.keys())

teams=payload["data"]
#inspecting
print(type(teams))
# print(len(teams))
# print(teams[0])

# for i in teams:
#     print(i["full_name"])

df=pd.DataFrame(teams)
print("Columns:", df.columns.to_list)
print("First Record: ")
print(df.iloc[0])  #integer location -gets the first row of the data frame

print("Pagintation:",payload.get("meta"))

snapshot= {
    "retrieved_at":datetime.now(timezone.utc).isoformat(),
    "endpoint":"https://api.balldontlie.io/v1/teams",
    "query_params":{},
    "response":payload,
}

output_folder=Path("data/raw")
output_folder.mkdir(parents=True,exist_ok=True)  #parents True lets create the praent folder too

output_file=output_folder/"teams_response.json"

with output_file.open("w",encoding="utf-8") as file:
    json.dump(snapshot,file,indent=2)  #.dumps make the dictionary into JSON