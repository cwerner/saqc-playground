from prefect import task, flow

# flow
@flow(name="flow2_ingest")
def flow1(*, src_path="/pd/raw_data"):
    pass

def main():
    flow1()

if __name__ == "__main__":
    main()
