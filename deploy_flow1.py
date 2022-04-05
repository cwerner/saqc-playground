from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule

DeploymentSpec(
    name="flow1-deployment",
    flow_location="./flows/flow1_lvl0-check.py",
    tags=['demoflows','test'],
    parameters={
        'src_path': '/netapp/rawdata/fendt/micromet/raw/slow_response',
        'year': 2022,
        'doy': 20,
        },
    schedule=CronSchedule(cron="*/5 * * * *"),
)
