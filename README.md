 Titanic Survival Prediction - Machine Learning Project

## Project Overview

This project is a binary classification machine learning project based on the Titanic dataset. The main goal is to build a model that predicts whether a passenger survived the Titanic disaster.

The project covers the complete machine learning workflow, including data loading, cleaning, feature preparation, preprocessing, model training, evaluation, cross-validation, hyperparameter tuning, and final model recommendation.

---

## 1. Problem Framing

### Business Question

Can we predict whether a Titanic passenger survived based on passenger information such as passenger class, sex, age, family information, fare, and port of embarkation?

This prediction can help understand which passenger characteristics were associated with survival and demonstrate how a classification model can be used to make predictions from structured data.

### Problem Type

This is a **binary classification problem**.

The target column contains two possible classes:

- `0` = Did not survive
- `1` = Survived

### Target Variable (y)

The target variable is:

```text
Survived
Feature Variables (X)

The following columns were used as features:

Pclass
Sex
Age
SibSp
Parch
Fare
Embarked

The following columns were not used as model features:

Survived — target variable
PassengerId — identifier column
Name — high-cardinality text column
Ticket — high-cardinality identifier-like column
Cabin — removed during cleaning because of a large number of missing values
2. Data Loading and Cleaning

The dataset was loaded independently for this project using pandas. The cleaning code is self-contained and does not import any files or cleaning code from Part 1.

Cleaning Steps
Duplicate Rows

Duplicate rows were removed using:

df.drop_duplicates()

This was done to prevent repeated records from affecting model training.

Missing Age Values

The missing values in the Age column were filled using the median age.

The median was selected because it is less affected by extreme values than the mean.

Missing Embarked Values

The missing values in the Embarked column were filled using the most frequent category (mode).

This is suitable because Embarked is a categorical column.

Cabin Column

The Cabin column was dropped because it contained a very large number of missing values.

Using this column directly would require a large amount of imputation and could introduce unnecessary noise into the model.

3. Feature Preparation

The data was split into training and testing sets before fitting the encoder or scaler.

The following split was used:

Training data: 80%
Testing data: 20%
random_state: 42

The train/test split was performed using train_test_split.

Categorical Features

The categorical features were:

Sex
Embarked

These columns do not have a natural numerical order, so One-Hot Encoding was used.

One-Hot Encoding converts categories into separate binary columns. This prevents the model from incorrectly assuming that one category is numerically greater or smaller than another.

The encoder used:

OneHotEncoder(handle_unknown="ignore")

The handle_unknown="ignore" option prevents errors if an unseen category appears in the test data.

Numerical Features

The numerical features were:

Pclass
Age
SibSp
Parch
Fare

These numerical features were standardized using:

StandardScaler

Standardization helps models that are sensitive to feature scale, especially Logistic Regression.

Data Leakage Prevention

The preprocessing steps were placed inside a scikit-learn Pipeline and ColumnTransformer.

The encoder and scaler were fitted only on training data and then used to transform the test data.

This prevents information from the test set from leaking into the training process.

4. Model Training and Evaluation

Since the target variable Survived contains two classes, this project uses classification models.

The following three models were trained:

Logistic Regression
Decision Tree Classifier
Random Forest Classifier

The primary evaluation metric is Binary F1-score.

The positive class is:

1 = Survived

F1-score was selected because it combines precision and recall into a single metric.

5. Class Balance Check

The target class distribution was:

Class 0: 61.62%
Class 1: 38.38%

The minority class represents approximately 38.38% of the dataset.

Since this is greater than the required 35% threshold, the class distribution was considered balanced enough.

Therefore, no SMOTE, oversampling, or undersampling technique was applied.

6. Model Comparison

The models were compared using the primary metric, Binary F1-score.

Rank	Model	Accuracy	Precision	Recall	F1-Score
1	Logistic Regression	0.8101	0.7857	0.7432	0.7639
2	Random Forest	0.8101	0.7941	0.7297	0.7606
3	Decision Tree	0.7765	0.7179	0.7568	0.7368
Model Recommendation

Logistic Regression is the recommended model for this project because it achieved the highest Binary F1-score of 0.7639 among the three evaluated models. Since Binary F1-score was selected as the primary metric, the final model ranking and recommendation are based on this metric. Logistic Regression also achieved approximately 81% accuracy and provides a simpler and more interpretable model compared with the tree-based models. Therefore, Logistic Regression would be the model I would choose to ship for this prediction task.

7. Cross-Validation

The best-performing model from the initial comparison was Logistic Regression.

A 5-fold Stratified Cross-Validation was performed using the complete preprocessing and modeling pipeline.

Stratified K-Fold was used because this is a classification problem and it helps maintain a similar class distribution across the folds.

F1-score for Each Fold
Fold 1: 0.7050
Fold 2: 0.7287
Fold 3: 0.7040
Fold 4: 0.7153
Fold 5: 0.7681
Cross-Validation Results
Mean F1-score: 0.7242
Standard Deviation: 0.0237

The preprocessing steps were included inside the Pipeline. Therefore, the encoder and scaler were fitted independently inside each training fold instead of using a globally pre-fitted preprocessing object.

8. Hyperparameter Tuning

GridSearchCV was used to tune the Logistic Regression model.

The following hyperparameters were searched:

C

The C parameter controls the strength of regularization.

Values searched:

0.01, 0.1, 1, 10
Solver

The solver controls the optimization algorithm used by Logistic Regression.

Values searched:

liblinear
lbfgs

The same complete Pipeline containing the preprocessing steps and Logistic Regression model was passed to GridSearchCV.

Best Parameters
C = 1
solver = liblinear
Best Cross-Validation F1-score
0.7179

The hyperparameter search used Binary F1-score as the scoring metric, which is the primary metric selected for this binary classification problem.

9. Final Conclusion

Three classification models were trained and evaluated. Logistic Regression achieved the highest Binary F1-score of 0.7639 on the test set and was selected as the recommended model.

Cross-validation and hyperparameter tuning were also performed to improve and validate the model. The final selected Logistic Regression configuration used C=1 and the liblinear solver.

Overall, the project demonstrates a complete machine learning workflow from data cleaning and preprocessing to model evaluation, cross-validation, hyperparameter tuning, and final model selection.

10. Tools and Libraries
Python
pandas
NumPy
scikit-learn
Google Colab
GitHub
11. AI Assistance

ChatGPT was used as a learning and development assistant during this project.

It helped with:

Understanding machine learning concepts
Explaining preprocessing and pipeline steps
Debugging errors
Understanding evaluation metrics
Structuring the README
Reviewing code logic

The final workflow, dataset preparation, model training, evaluation, and results were reviewed and run as part of this project.