import os
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torch.utils.data import Dataset, DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import matplotlib.pyplot as plt

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCHSIZE = 32
EPOCHS = 100
INPUT_FEATURES = 24

FOOD_ID_DICT = {
    "0.0": "Kabayaki sea bream fillet",
    "1.0": "Spam",
    "2.0": "apple -sliced-",
    "3.0": "cabbage",
    "4.0": "coin",
    "5.0": "creamy tofu",
    "6.0": "creamy tofu -without sauce-",
    "7.0": "cucumber",
    "8.0": "egg tofu",
    "9.0": "firm tofu",
    "10.0": "fish cake",
    "11.0": "fried chicken cutlet",
    "12.0": "fried potato",
    "13.0": "grilled pork",
    "14.0": "guava -sliced-",
    "15.0": "mustard greens",
    "16.0": "pig blood curd",
    "17.0": "pig liver",
    "18.0": "pineapple",
    "19.0": "pumpkin",
    "20.0": "red grilled pork",
    "21.0": "soy egg",
    "22.0": "sweet potato leaves"
}

def calculate_rmse_per_food_item(preds, targets, ids):
    unique_ids = torch.unique(ids).numpy()
    rmse_per_food_item = {}
    for uid in unique_ids:
        indices = ids == uid
        rmse = torch.sqrt(F.mse_loss(preds[indices], targets[indices]))
        rmse_per_food_item[uid] = rmse.item()
    return rmse_per_food_item

def plot_rmse_per_food_item(rmse_per_food_item, food_id_dict, filename='rmse_per_food_item.png'):
    # Sort the rmse_per_food_item by the food ID keys and match them with food names using the food_id_dict
    sorted_items = sorted(rmse_per_food_item.items(), key=lambda x: float(x[0]))
    labels = [food_id_dict[str(uid)] for uid, _ in sorted_items]
    rmse_values = [rmse for _, rmse in sorted_items]

    plt.figure(figsize=(15, 10))  # Increased figure size for readability
    bars = plt.bar(labels, rmse_values, color='skyblue')
    plt.xlabel('Food Type', fontsize=12)
    plt.ylabel('RMSE', fontsize=12)
    plt.title('RMSE for Each Food Type', fontsize=14)
    plt.xticks(rotation=90, fontsize=10)  # Rotate labels to prevent overlap

    # Add the text labels above the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom', fontsize=8)
    
    # Save the figure to a file
    plt.savefig(filename, bbox_inches='tight')  # bbox_inches='tight' minimizes the extra whitespace around the figure.

def define_model():
    class MLP(nn.Module):
      def __init__(self):
          super().__init__()
          self.fc1 = nn.Linear(INPUT_FEATURES, 97)
          self.fc2 = nn.Linear(97, 128)
          self.fc3 = nn.Linear(128, 1)
          self.relu = nn.ReLU()
          self.dropout1 = nn.Dropout(0.3336182856425359)
          self.dropout2 = nn.Dropout(0.21470682429854432)

      #this is mandatory
      def forward(self, x):
          x = self.relu(self.fc1(x))
          x = self.dropout1(x)
          x = self.relu(self.fc2(x))
          x = self.dropout2(x)
          x = self.fc3(x)
          return x

    return MLP()

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

def main():
    # Generate the model.
    model = define_model().to(DEVICE)
    criterion = nn.MSELoss() # mean squared error loss
    optimizer = optim.RMSprop(model.parameters(), lr=0.0023892935186788345)

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
        print(f'Epoch {epoch+1}/{EPOCHS}, MSE: {mse_loss:.4f}')
        print(f'RMSE:{rmse_loss:.4f}')

    # Model evaluation modifications start here
    model.eval()
    all_preds = []
    all_targets = []
    all_ids = []
    with torch.no_grad():
        for batch_idx, (data, target, id) in enumerate(valid_loader):
            data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
            output = model(data)
            all_preds.append(output.view(-1))
            all_targets.append(target.view(-1))
            all_ids.append(id)

    # Concatenate all batches
    all_preds = torch.cat(all_preds).cpu()
    all_targets = torch.cat(all_targets).cpu()
    all_ids = torch.cat(all_ids).cpu()

    # Calculate RMSE per food item
    rmse_per_food_item = calculate_rmse_per_food_item(all_preds, all_targets, all_ids)

    # Plot RMSE per food item
    plot_rmse_per_food_item(rmse_per_food_item, FOOD_ID_DICT)

    return rmse_loss


if __name__ == "__main__":
    main()