from prefect import task, flow, get_run_logger
from pathlib import Path
import datetime
import tempfile
from string import Template
import pandas as pd
from typing import Optional

from sshfs import SSHFileSystem

def check_file_exists(location: Path | str):
    """Check if file exists"""
    return Path(location).is_file()

@task(description="Source data from rawdata and transform it into pandas dataframe.", tags=["ssh"])
def load_data(
    location: Path | str, 
    *, 
    year: Optional[int] = None, 
    doy: Optional[int] = None, 
    template_name: Template = Template("Fen_M_${year_short}_${doy}.dat"),
    ) -> pd.DataFrame:

    if not year:
        year = datetime.datetime.now().year
    year_short = int(str(year)[2:])

    if not doy:
        doy = datetime.datetime.now().timetuple().tm_yday - 1

    name = template_name.safe_substitute({'year_short': year_short, 'doy': f"{doy:03d}"})

    fs = SSHFileSystem(
        'imk-ifu-wank.imk-ifu.kit.edu',
        client_keys=['/Users/werner-ch/.ssh/id_rsa']
    )

    # read header info
    with fs.open(Path(location) / "Fen_M_header.csv", "r") as fheader:
        colnames = fheader.readline()[:-1].split(",")

    # read raw data
    with tempfile.TemporaryDirectory() as tmp:
        source_file = Path(location) / str(year) / name
        tmp_file = Path(tmp) /  name
        fs.get_file(source_file, Path(tmp) /  name)

        df = pd.read_csv(tmp_file, names=colnames, header=None, na_values="NAN", parse_dates=['TIMESTAMP'])
    
    return df


# flow
@flow(name="flow1-lvl0-check")
def flow1(
    src_path: str="/netapp/rawdata/fendt/micromet/raw/slow_response", 
    year: Optional[int]=None,
    doy: Optional[int]=None,
    ):
    logger = get_run_logger()

    df = load_data(src_path, year=year, doy=doy)
    logger.info(df.result().head())
    return

def main():
    flow1()

if __name__ == "__main__":
    main()
