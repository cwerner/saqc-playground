from prefect import task, flow, get_run_logger

import pandas as pd
from typing import Any
import os

from stantic.server import Server
from stantic.models import Datastream, Thing

from pathlib import Path

from dotenv import load_dotenv

from src.tasks import load_data

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
@flow(name="flow2_ingest")
def flow2_ingest(df: pd.DataFrame):
    url = os.getenv("FROST_URL")
    server = intialize_server(url)

    #df = load_data("/netapp/rawdata/fendt/micromet/raw/slow_response", year=year, doy=doy)

    # get data - we need a better mapping service (json on s3)?
    # 140: temp, 144: precip
    for id, colname in zip([140, 144], ["airtemp_avg", "ramount"]):
        push_data(server, df=df[[colname]], datastream_id=id)



def main():

    df = pd.DataFrame(
        data={'airtemp_avg': [2, 2, 3, 4, 3], 'ramount': [0, 0, 0, 0.1, 1.2]}, 
        index=pd.date_range(start='1/1/2018', end='1/5/2018')
        )

    flow2_ingest(df)


if __name__ == "__main__":
    main()
