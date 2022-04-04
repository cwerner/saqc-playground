# 🚀 Getting started

This section shows you how the components of this setup are interlinked. Let's dive in...

(sta-scheme)=
:::{mermaid}
:caption: Data Flow Integration

flowchart LR
    id1("Station 🗼") -- ftp --> id2("File Server 📁")
    subgraph "Prefect Data Flow Orchestration (🤖)"
    id2 --  "F1 🤖"--> id3("Lvl0 Check (GE) 🔎") -- "F2 🤖: STA Ingest" --> id5[("Frost ❄️")]
    id5 -- "F3 🤖"--> id6("Lvl1 Check (SaQC) 🔎")
    id6 -.-> id7[("Archive 🗄")]
    end
    id5 <--access--> id9("Grafana 📊")
    id6 --reporting--> id8("PI 🧑‍🔬")
    id8 --approve--> id7
    id7 <-- access --> id10("WWW 🌍")
    click id5 href "http://172.27.80.119:8093/FROST-Server/v1.1" _blank
    click id7 href "https://thredds.imk-ifu.kit.edu:9670/thredds/catalog.html" _blank
:::

## Summary

:::{admonition} Tools

|         | type       | description           | reference
| :---    | :----:     | :----:                | ----:
| stantic | 🐍 lib     | SensorThings API interface library | [code](https://github.com/cwerner/stantic), [docs](https://cwerner.github.io/stantic/)
| SaQC    | 🐍 lib     | QC library            | [code](https://git.ufz.de/rdm-software/saqc), [docs](https://rdm-software.pages.ufz.de/saqc/index.html)
| Prefect | 🐍 lib, ✨ service | Orchestration and dataflow automation platform | [code](https://github.com/PrefectHQ/prefect), [docs](https://orion-docs.prefect.io), [home](https://www.prefect.io)
| FROST   | ✨ service   | Server implementation of the OGC SensorThings API | [code](https://github.com/FraunhoferIOSB/FROST-Server), [docs](https://fraunhoferiosb.github.io/FROST-Server/), [home](https://www.iosb.fraunhofer.de/de/projekte-produkte/frostserver.html)
| THREDDS | ✨ service   | Thematic Real-time Environmental Distributed Data Services data server | [code](https://github.com/Unidata/tds), [docs](https://docs.unidata.ucar.edu/tds/5.3/userguide/index.html), [home](https://www.unidata.ucar.edu/software/tds/)

:::

### Data ingestion
Data at IMK-IFU is currently reaching the institute via `ftp` upload or `nextcloud-based sync` schedules. This usually happens once or twice a day.

### First Quality Control
Right after data is transfered to the institute, a basic data quality check is performed. Here, simple things as size of new data package, number of columns, nodata occurance etc. are validated. All these checks work on daily data packages so trends or trend deviations can not be detected. Missing data or any failed data expectations immediately trigger a warning email since they indicate measurement or transfer failures.

### Ingestion into STA Frost Server
Once data passed the initial stage, a subset of datastreams is parsed and loaded into the [FROST server](http://172.27.80.119:8093/FROST-Server/v1.1) using a Prefect Flow and the [stantic python library](https://github.com/cwerner/stantic). Grafana dashboards allow a quick inspection into raw data.

### Second Quality Control
In this stage data is checked in a more thorough way. In addition to simple range checks, checks for trend breaks or other unexpected occurences are performed. These checks require multiple batches of data and thus cannot run at the ingest stage. This quality control stage will either run daily or weekly. [SaQC](https://git.ufz.de/rdm-software/saqc) will be used to analyse a running window of data (i.e. previous 30 or 60 days) and aid in preparing a report for the relevant PI. After approval by the PI, the data will be marked as ready for archival. 

### Data archive
After the approval of an PI the data will be ingested into the final datasets. This might be timeseries data on [THREDDS](https://thredds.imk-ifu.kit.edu:9670/thredds/catalog.html) or other data formats. 

