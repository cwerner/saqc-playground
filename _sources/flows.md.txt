# 🚰 Data Flows

In this section the core Prefect data flows are listed (see [flowchart](fig-data-flow-scheme)).


(flows-flow1)=
## 1. Check - Level 0

:::{admonition} Summary
Initial loading and validation of new data detected in the IMK-IFU `rawdata` folder.
:::

:::{admonition} Operation
:class: seealso
scheduled: daily, 8:00h
:::

:::{literalinclude} ../../flows/flow1_lvl0-check.py
---
language: python
start-after: "# flow\n"
end-before: "def main"
---
:::

(flows-flow2)=
## 2. Ingest

:::{admonition} Summary
Upload data to the appropriate datastreams in the `FROST` server using the `stantic`
library.
:::

:::{admonition} Operation
:class: seealso
triggered: success of flow [](flows-flow1)
:::

:::{literalinclude} ../../flows/flow2_ingest.py
---
language: python
start-after: "# flow\n"
end-before: "def main"
---
:::

## 3. Check - Level 1

## 4. Archive

