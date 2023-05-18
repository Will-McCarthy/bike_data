import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

# Load the dataset into a Pandas DataFrame
data = pd.read_csv('North_American_Bikes.csv')

# Select the columns of interest
columns_to_keep = ['Price in USD', 'Brand', 'Year', 'Rear Travel', 'Wheel Size','Condition','Material']
pre_downselect = data
# Keep only the selected columns
data = data[columns_to_keep]

# Remove rows with missing values
data = data.dropna()

# Compute the IQR for each numeric column
Q1 = data['Price in USD'].quantile(0.25)
Q3 = data['Price in USD'].quantile(0.75)
IQR = Q3 - Q1

# Define the threshold for outliers
threshold = 1.5

# Filter outliers by applying the threshold
data = data[~((data['Price in USD'] < (Q1 - threshold * IQR)) | (data['Price in USD'] > (Q3 + threshold * IQR)))]

# Split the data into features (X) and target variable (y)
X = data.drop('Price in USD', axis=1)
y = data['Price in USD']

# Perform one-hot encoding on categorical features
X = pd.get_dummies(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Create a decision tree regressor
treeModel = DecisionTreeRegressor()
linearModel = LinearRegression()

# Train the model on the training set
treeModel.fit(X_train, y_train)
linearModel.fit(X_train, y_train)

# Make predictions on the test set
y_predTree = treeModel.predict(X_test)
y_predLinear = linearModel.predict(X_test)

# results_df = pd.DataFrame({'Actual Price': y_test, 'Predicted Price': y_pred})
#
# # Retrieve the original unencoded columns
# original_columns = ['Year', 'Brand', 'Title', 'Rear Travel', 'Wheel Size', 'Condition', 'Material']
# original_data = pre_downselect[original_columns]
#
# # Merge the original unencoded columns with the results DataFrame
# results_df = pd.concat([results_df, original_data], axis=1)
#
# # Print the results
# pd.set_option('display.max_rows', None)
# print(results_df.head(30))


# Evaluate the model
mse = mean_squared_error(y_test, y_predLinear)
mpe = mean_absolute_percentage_error(y_test, y_predLinear)
r2 = r2_score(y_test, y_predLinear)
print('')
print('Linear Model Results')
print("Mean Squared Error:", mse)
print("Mean Percentage Error:", mpe)
print("R2 Score:", r2)


# Evaluate the model
mse = mean_squared_error(y_test, y_predTree)
mpe = mean_absolute_percentage_error(y_test, y_predTree)
r2 = r2_score(y_test, y_predTree)
print('')
print('Decision Tree Model Results')
print("Mean Squared Error:", mse)
print("Mean Percentage Error:", mpe)
print("R2 Score:", r2)
print('')
