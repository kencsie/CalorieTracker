import os
import pandas as pd
import optuna
from optuna.trial import TrialState
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torch.utils.data import Dataset, DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCHSIZE = 32
EPOCHS = 100
INPUT_FEATURES = 13
TRIAL = 1000


def define_model(trial):
    # We optimize the number of layers, hidden units and dropout ratio in each layer.
    n_layers = trial.suggest_int("n_layers", 1, 3)
    layers = []

    in_features = INPUT_FEATURES
    for i in range(n_layers):
        out_features = trial.suggest_int("n_units_l{}".format(i), 4, 128)
        layers.append(nn.Linear(in_features, out_features))
        layers.append(nn.ReLU())
        p = trial.suggest_float("dropout_l{}".format(i), 0.2, 0.5)
        layers.append(nn.Dropout(p))

        in_features = out_features
    layers.append(nn.Linear(in_features, 1))

    return nn.Sequential(*layers)

def get_csv_data():
    def load_food_csv():
        # Load Food csv.
        csv_path = os.path.join(os.getcwd(), 'output.csv')
        return pd.read_csv(csv_path)

    def csv_remove_nan(data):
        # Drop row without mass and area
        data.dropna(subset=['area'], inplace=True)
        data.dropna(subset=['mass'], inplace=True)
        return data
    
    def csv_drop_less_than_30(data):
        # Calculate ID counts
        value_counts = data['object_id'].value_counts()
        
        # Drop row less than 30
        keep_table = value_counts >= 30
        ids_to_keep = value_counts[keep_table].index
        return data[data['object_id'].isin(ids_to_keep)]

    def csv_drop_unnecessary_columns(data):
        # Drop unnecessary columns
        return data.drop(columns=['object_id','mass', 'image_name', 'x_center', 'y_center', 'width', 'height'], axis=1)

    def csv_one_hot_encode(data):
        # One-hot encode the 'object_id' column
        encoder = OneHotEncoder(sparse_output=False)
        X_cat_one_hot = encoder.fit_transform(data['object_id'].values.reshape(-1, 1))

        # Convert to a DataFrame
        X_cat_one_hot_df = pd.DataFrame(X_cat_one_hot, columns=encoder.get_feature_names_out(['object_id']))
        return X_cat_one_hot_df

    # Data Preprocessing
    data = load_food_csv()
    data = csv_remove_nan(data)
    data = csv_drop_less_than_30(data)

    # Drop unnecessary features
    X = csv_drop_unnecessary_columns(data)
    # concatinate the one-hot encoded columns
    X.reset_index(drop=True, inplace=True)
    X = pd.concat([X, csv_one_hot_encode(data)], axis=1)
    # Generate feature and target data
    X = StandardScaler().fit_transform(X)
    y = data['mass'].copy()
    #print(f'X.shape:{X.shape}, y.shape:{y.shape}, object_id.shape:{data["object_id"].shape}')

    return X, y, data['object_id']

def get_csv_dataloader(X, y, X_object_id):
    # Custom Dataset class
    class CustomDataset(Dataset):
        def __init__(self, inputs, targets, ids):
            self.inputs = inputs
            self.targets = targets
            self.ids = ids

        def __len__(self):
            return len(self.inputs)

        def __getitem__(self, idx):
            return self.inputs[idx], self.targets[idx], self.ids[idx]

    # Step 1: Split the data while preserving food IDs
    X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
        X, y, X_object_id, test_size=0.2, random_state=42
    )

    # Convert to PyTorch tensors
    X_train, X_test, y_train, y_test, ids_train, ids_test = map(
        torch.tensor, (X_train, X_test, y_train.to_numpy(), y_test.to_numpy(), ids_train.to_numpy(), ids_test.to_numpy())
    )

    # Step 2: Create Tensor datasets with food IDs
    train_ds = CustomDataset(X_train.float(), y_train.float(), ids_train.float())
    test_ds = CustomDataset(X_test.float(), y_test.float(), ids_test.float())

    # Data loaders
    train_loader = DataLoader(train_ds, batch_size=BATCHSIZE, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=BATCHSIZE, shuffle=False)

    return train_loader, test_loader

def objective(trial):
    # Generate the model.
    criterion = nn.MSELoss() # mean squared error loss
    model = define_model(trial).to(DEVICE)

    # Generate the optimizers.
    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "RMSprop", "SGD"])
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    optimizer = getattr(optim, optimizer_name)(model.parameters(), lr=lr)

    # Get the food dataset.
    X, y, X_object_id = get_csv_data()
    train_loader, valid_loader = get_csv_dataloader(X, y, X_object_id)

    # Training of the model.
    for epoch in range(EPOCHS):
        model.train()
        for batch_idx, (data, target, id) in enumerate(train_loader):
            data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target.view_as(output))
            loss.backward()
            optimizer.step()

        # Validation of the model.
        model.eval()
        mse_loss = 0
        count = 0
        with torch.no_grad():
            for batch_idx, (data, target, id) in enumerate(valid_loader):
                data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
                output = model(data)
                mse_loss += criterion(output, target.view_as(output))
                count += 1

        mse_loss /= count
        rmse_loss = torch.sqrt(mse_loss).item()

        trial.report(rmse_loss, epoch)

        # Handle pruning based on the intermediate value.
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return rmse_loss


if __name__ == "__main__":
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=TRIAL, timeout=600)

    pruned_trials = study.get_trials(deepcopy=False, states=[TrialState.PRUNED])
    complete_trials = study.get_trials(deepcopy=False, states=[TrialState.COMPLETE])

    print("Study statistics: ")
    print("  Number of finished trials: ", len(study.trials))
    print("  Number of pruned trials: ", len(pruned_trials))
    print("  Number of complete trials: ", len(complete_trials))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: ", trial.value)

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))