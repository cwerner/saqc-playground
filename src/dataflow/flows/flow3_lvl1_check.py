from prefect import task, flow, get_run_logger

import pandas as pd
from typing import Any
import os

from stantic.server import Server
from stantic.models import Datastream, Thing

import datetime

from saqc import SaQC

from dotenv import load_dotenv


load_dotenv()


@task(description="return stantic server instance to specified FROST server")
def intialize_server(url: str):
    """initialize a Server instance to connect to a FROST server"""
    server = Server(url=url)
    if not server.is_alive:
        raise ValueError(f"Server is not alive at URL {url}")
    return server


@task(description="pull windowed subset of data from given datastream of FROST server")
def pull_data(server: Server, datastream_id:int) -> pd.DataFrame:
    logger = get_run_logger()

    # 140 = temp
    temp_stream = server.get(Datastream, id=datastream_id, tag_off=True)    # TERENO Fendt site
    logger.info(temp_stream)

    start_date = datetime.date.today() - datetime.timedelta(days=51)
    end_date = datetime.date.today() - datetime.timedelta(days=44)

    df = server.pull_data(temp_stream, dt_min=start_date, dt_max=end_date)

    return df


@task(description="validate datastreams with SaQC")
def check_data(data: pd.DataFrame, id:int) -> SaQC:
    """check data properties with saqc"""

    qc = SaQC(data=data, scheme="simple")

    if id == 140:
        qc = (qc.flagRange("result", min=-6, max=10)
                .flagConstants("result", thresh=0.1, window=10))
    elif id == 144:
        qc = (qc.flagRange("result", min=0, max=200)
                .flagConstants("result", thresh=0.1, window=50))
    else:
        raise NotImplementedError

    return qc



@task(description="reporte saqc validation (email or internal page)")
def reporting(payload: Any):
    logger = get_run_logger()

    logger.info("Writing report/ sending email")
    logger.info(f" for datastreams {payload.keys()}")


# flow
@flow(name="flow3_lvl1_check")
def flow3_lvl1_check(url: str):

    server = intialize_server(url)

    # get data
    # 140: temp, 144: precip

    # TODO: can we write SaQC validations as json?

    payload = {}
    for id in [140, 144]:
        df = pull_data(server, datastream_id=id)
        qc = check_data(df, id)
        payload[id] = qc

    reporting(payload)




if __name__ == "__main__":
    url = os.getenv("FROST_URL")
    flow3_lvl1_check(url)
