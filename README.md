# Statistics collection extension for Dialog Flow Framework
dff_node_stats is package, that extends basic [dialog_flow_engine](https://github.com/deepmipt/dialog_flow_engine) by adding statistic collection **and** dashboard for visualization.

# Installation
Installation:
```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt

```
# First examples
```bash
# run dff dialog bot and collect stats
python examples/collect_stats.py
# run dashboard (make sure you installed the lib with [streamlit] extra)
# It can take several minutes
streamlit run examples/run_dashboard_for_stats.py
# run api and follow to swagger by http://localhost:8000/docs
# note that [api] install option is required.
```
# Code snippets

Insert stats in your dff code:
```python
# import dependencies
from df_engine.core.plot import Plot
from df_engine.core.actor import Actor
from dff_node_stats import Stats, Saver
# ....
# Define a plot and an actor
plot = Plot(foo)
actor = Actor(bar, baz)

# Define file for stats saving
stats = Stats(
    saver=Saver("csv://examples/stats.csv")
)
# As an alternative, you can use a database. Currently, Clickhouse and Postgreql are supported
stats = Stats(
    saver=Saver("postgresql://user:password@localhost:5432/default")
)

# You can optionally add predefined Collectors to gather additional data
from dff_node_stats import collectors as DSC
from dff_node_stats import Stats, Saver

stats = Stats(
    saver=Saver("csv://examples/stats.csv"),
    collectors=[
        DSC.NodeLabelCollector()
    ]
)
# Or define your own Collector. 
# It should implement methods and properties, defined in the Collector protocol,
# which will make it compatible with multiple databackends.
# For more information see dff_node_stats.collectors


# Add handlers to actor
stats.update_actor_handlers(actor, auto_save=False)

# ....
# Handle user requests
# ....

```
Dashboard on stored data (\[streamlit\] extra required!):
```python
from dff_node_stats import Stats, Saver
from dff_node_stats.widgets.streamlit import StreamlitDashboard

stats = Stats(
    saver=Saver("csv://examples/stats.csv")
)

streamlit_dashboard = StreamlitDashboard(df)
streamlit_dashboard()
```

http-api on stored data (\[api\] extra required!om dff_node_stats import Stats, Saver
```python
from dff_node_stats.api import api_run
from dff_node_stats import Stats, Saver

stats = Stats(
    saver=Saver("csv://examples/stats.csv"),
    collectors=[
        DSC.NodeLabelCollector()
    ]
)

api_run(stats.dataframe)
```


# Run Other Examples:
```bash
# run dff dialog bot and collect stats
python examples/collect_stats.py
# or this one, they have differences only in a dialog scripts
python examples/collect_stats_vscode_demo.py

# run dashboard (make sure you installed the lib with [streamlit] extra)
streamlit run examples/run_dashboard_for_stats.py
# run api and follow to swagger by http://localhost:8000/docs
# note that [api] install option is required.
python examples/get_stats_by_api.py
# jupyter version of the dashboard can be launched by:
jupyter notebook examples/run_dashboard.ipynb
# you need to have [jupyter] option installed.
```