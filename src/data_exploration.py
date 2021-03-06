# %% About the problem
"""
About the problem:
* This is a multi-label problem
* The targets have 206 features (binary) with each observation containing
several combinations of features
* A gbm could be used but this would entail training a separate gbm for each
feature since they don't support multi-label processing. This would require a
lot of time.
* In other words, in a multilabel problem the outcome is represented not by
one column but by several columns and each column would require its own
model.
* A neural network would overcome this problem.
"""
# %% Packages
import pandas as pd
import matplotlib.pyplot as plt
import glob

# %% Data importation
file_paths = glob.glob(pathname="../inputs/*.csv")

sample_submission = pd.read_csv(file_paths[0])
test_features = pd.read_csv(file_paths[1])
train_drug = pd.read_csv(file_paths[2])
train_features = pd.read_csv(file_paths[3])
train_targets_nonscored = pd.read_csv(file_paths[4])
train_targets_scored = pd.read_csv(file_paths[5])

# %% Feature exploration
train_features.head()
train_features.shape
train_features.sig_id.nunique()
train_features.cp_type.value_counts()

# %% Feature visualisation
g_cols = [col for col in train_features.columns if "g-" in col]
gs = train_features[g_cols][:1].values.reshape(-1, 1)
plt.plot(gs)
plt.plot(sorted(gs))

train_features["g-0"].plot(kind="hist")

train_features["c-0"].plot(kind="hist")

# %% Target exploration
# Some labels demonstrate extreme class imqbalance
train_targets_scored.head()
train_targets_scored.shape
train_targets_scored.sum()[1:].sort_values()
train_targets_scored.autotaxin_inhibitor.value_counts()
