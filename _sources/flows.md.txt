# 🚰 Data Flows

In this section the core Prefect data flows are listed (see [flowchart](fig-data-flow-scheme)).


(flows-flow1)=
## 1. Check - Level 0

:::{admonition} Summary
Initial loading and validation of new data batch detected in the IMK-IFU `rawdata` folder.
:::

:::{admonition} Operation
:class: seealso
scheduled: daily, 8:00h
:::

:::{literalinclude} ../../src/dataflow/flows/flow1_lvl0-check.py
---
language: python
start-after: "# flow"
end-before: "if __name__"
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

:::{literalinclude} ../../src/dataflow/flows/flow2_ingest.py
---
language: python
start-after: "# flow"
end-before: "if __name__"
---
:::

## 3. Check - Level 1

:::{admonition} Summary
More indepth check if new data uwing the `SaQC` library. In this check, preceeding data is also considered (i.e. to detect unplausible trend shifts).
:::

:::{admonition} Operation
:class: seealso
scheduled: daily, 9:00h
:::

:::{literalinclude} ../../src/dataflow/flows/flow3_lvl1_check.py
---
language: python
start-after: "# flow"
end-before: "if __name__"
---
:::

## 4. Archive

:::{admonition} Summary
Creation of data archives, catalog entries and summary products.
:::

:::{admonition} Operation
:class: seealso
scheduled: daily, weekly or monthly
:::

TBD