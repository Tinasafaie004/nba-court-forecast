import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
import time
from datetime import datetime,timezone
from pathlib import Path

load_dotenv(override=True)

api_key=os.getenv("BALLDONTLIE_API_KEY")

if not api_key:
    raise ValueError("Missing BALLDONTLIE_API_KEY in .env")


output_folder=Path("data/raw/games/2024")
output_folder.mkdir(parents=True, exist_ok=True) 

def save_page(end_point,query_params,payload,output_file):
    
    snapshot={
        "retrieved_at":datetime.now(timezone.utc).isoformat(),
        "endpoint":end_point,
        "query_params":query_params,
        "response":payload
    }

    with output_file.open("w",encoding="utf-8") as file:
        json.dump(snapshot,file,indent=2)  #json.dump turns python file  to a JSON 




def get_request(end_point,params,headers,timeout):
    return requests.get(
        end_point,
        params=params,   #requests turns dict into a web address and SKIPS None vals(...games?seasons%5B%5D=2024&per_page=5)
        headers=headers,
        timeout=timeout
    )

#ROUND 1:

keep_looping=True
counter=0
end_point="https://api.balldontlie.io/v1/games"
next_cursor=None

while keep_looping:
    #testing
    # if counter==3:
    #     break

    counter+=1

    #we're creating one file per page for safety reasons:
    #if the wifi is dow, API is down, 429 (too many requets) , the pages that rea already save are still there
    query_params={"seasons[]":2024, "per_page":100,"cursor":next_cursor}

    output_file=output_folder/f"page_{counter:03d}.json"

    #CACHING :
    #1.no new request: already exists is loaded from the file, with no request and no sleep // so only missing files are downloaded
    #2.speed: a fully downloaded season finishes in about 1 second instead of 3 minutes
    if output_file.exists():
        with output_file.open(encoding="utf-8") as file:
            data=json.load(file)   #loads turn the file into a normal Python dict

        print(f"Page {counter}: from cache")
        next_cursor=data["response"]["meta"].get("next_cursor")


    else:
        response=get_request(end_point,query_params,{"Authorization":api_key},30)
        # print("Status:", response.status_code)
        response.raise_for_status()
        
        payload=response.json()  #parses JSON received over HTTP to python object
        #games_2024=payload["data"]
        #games_df=pd.DataFrame(games_2024)
        save_page(end_point,query_params,payload,output_file)
        print(f"Page {counter}: downloaded")

        next_cursor= payload["meta"].get("next_cursor")
        
        print("start")
        time.sleep(13) #60/5=12 --> +1 to be safe 13 seconds between requests
        print("13 seconds later")


    keep_looping=next_cursor is not None
    



