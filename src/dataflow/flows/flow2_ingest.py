from prefect import task, flow, get_run_logger

import pandas as pd
from typing import Any
import os

from stantic.server import Server
from stantic.models import Datastream, Thing

from pathlib import Path
from typing import Any

from dotenv import load_dotenv


load_dotenv()


@task(description="return stantic server instance to specified FROST server")
def intialize_server(url: str):
    """initialize a Server instance to connect to a FROST server"""
    server = Server(url=url)
    if not server.is_alive:
        raise ValueError(f"Server is not alive at URL {url}")
    return server


def check_file_exists(location: Path | str):
    """Check if file exists"""
    return Path(location).is_file()


@task(description="push latest data batch to FROST server")
def push_data(server: Server, df: pd.DataFrame, datastream_id:int):
    logger = get_run_logger()

    # 140 = temp
    stream = server.get(Datastream, id=datastream_id, tag_off=True)    # TERENO Fendt site
    logger.info(stream)
    logger.info("FAKE PUSH")
    #server.push_data(stream, df)
    return


# flow
@flow(name="flow2_ingest", description="subflow that is triggered by lvl0 check")
def flow2_ingest(df_json: str):
    url = os.getenv("FROST_URL")
    server = intialize_server(url)

    # we need to pass a serializable object (no plain pd.dataframe)
    df = pd.read_json(df_json, orient='split')
    
    # get data - we need a better mapping service (json on s3)?
    # 140: temp, 144: precip
    for id, colname in zip([140, 144], ["airtemp_avg", "ramount"]):
        push_data(server, df=df[[colname]], datastream_id=id)



if __name__ == "__main__":
    # test
    df = pd.DataFrame(
        data={'airtemp_avg': [2, 2, 3, 4, 3], 'ramount': [0, 0, 0, 0.1, 1.2]}, 
        index=pd.date_range(start='1/1/2018', end='1/5/2018')
        )

    # we need to oass a json around
    flow2_ingest(df.to_json(orient='split'))