import csv
from sklearn import svm
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression

# Read data in from file
with open("train.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)

    training_data = []
    for row in reader:
        training_data.append({
        "features": [float(cell) for cell in row[21:32]],
        "score": float(row[0])
        })

# Read data in from file
with open("val.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)

    testing_data = []
    for row in reader:
        testing_data.append({
        "features": [float(cell) for cell in row[21:32]],
        "score": float(row[0])
        })

X_training = [row['features'] for row in training_data]
y_training = [row['score'] for row in training_data]
reg = LinearRegression().fit(X_training, y_training)


X_testing = [row["features"] for row in testing_data]
y_testing = [row["score"] for row in testing_data]
predictions = reg.predict(X_testing)


print(mean_absolute_error(y_testing, predictions))
