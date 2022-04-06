from prefect import task, flow, get_run_logger
import pandas as pd
from typing import Optional

from ..src.tasks import load_data

from flows import flow2_ingest

@task(description="Validate new data with GreatExpectations lvl0 expectations.", tags=["ge"])
def validate_lvl0_data(df: pd.DataFrame):
    logger = get_run_logger()
    logger.info("GE Validation")

    # return True if validation was successful
    return True


# flow
@flow(name="flow1-lvl0-check")
def flow1_lvl1_check(
    src_path: str="/netapp/rawdata/fendt/micromet/raw/slow_response", 
    year: Optional[int]=None,
    doy: Optional[int]=None,
    ):
    logger = get_run_logger()

    df = load_data(src_path, year=year, doy=doy)
    status = validate_lvl0_data(df)

    # trigger subflow
    if status.result() == True:
        flow2_ingest(df)


    return df



if __name__ == "__main__":
    flow1_lvl1_check()
