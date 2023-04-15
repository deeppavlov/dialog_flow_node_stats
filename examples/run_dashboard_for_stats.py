import dff_node_stats
from dff_node_stats import collectors as DSC
from dff_node_stats.widgets.streamlit import StreamlitDashboard
from datasets import load_dataset

stats = dff_node_stats.Stats(
    saver=dff_node_stats.Saver("csv://examples/stats.csv"), collectors=[DSC.NodeLabelCollector(),DSC.RequestCollector(),DSC.ResponseCollector()]
)

df = stats.dataframe
from dff_node_stats.widgets import FilterType

filt = FilterType("Choose flow", "flow_label", lambda x, y: x == y, default=None)
filt2 = FilterType("Choose turn", "history_id", lambda x, y: x == y, default=None)

# Load a dataset for predictions
dataset = load_dataset("multi_woz_v22", split="test")
samples = sum([sample['turns']['utterance'] for sample in dataset], [])

# Prepare dialog model for recommendations
dialog_model = dff_node_stats.DialogModel()
dialog_model.fit(samples)

StreamlitDashboard(df, filters=[filt, filt2],
    dialog_model = dialog_model)()
