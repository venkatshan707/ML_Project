import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

# Configuration class using dataclass to define where to save the preprocessor object
@dataclass
class DataTransformationConfig:
    # Preprocessor file path where the object will be stored (as a pickle file)
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

# Main class for data transformation
class DataTransformation:
    def __init__(self):
        # Initialize the config with the preprocessor file path
        self.data_transformation_config = DataTransformationConfig()

    # Method to create the data transformer object (for preprocessing)
    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation, including 
        scaling numeric features and one-hot encoding categorical features.
        '''
        try:
            # List of numerical columns
            numerical_columns = ["writing_score", "reading_score"]

            # List of categorical columns
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Pipeline for numeric features:
            # 1. Imputing missing values with the median.
            # 2. Scaling the values to zero mean and unit variance.
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Imputing missing values with median
                    ("scaler", StandardScaler())  # Scaling features
                ]
            )

            # Pipeline for categorical features:
            # 1. Imputing missing values with the most frequent category.
            # 2. One-hot encoding the categories.
            # 3. Scaling the one-hot encoded values.
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Filling missing categorical values
                    ("one_hot_encoder", OneHotEncoder()),  # One-hot encoding the categorical values
                    ("scaler", StandardScaler(with_mean=False))  # Scaling (without centering) to normalize
                ]
            )

            # Logging the information about the columns
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # ColumnTransformer applies different transformations to numerical and categorical columns
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),  # Apply num_pipeline to numerical columns
                    ("cat_pipelines", cat_pipeline, categorical_columns)  # Apply cat_pipeline to categorical columns
                ]
            )

            return preprocessor  # Return the ColumnTransformer object

        except Exception as e:
            # Raise a custom exception if an error occurs
            raise CustomException(e, sys)

    # Method to initiate data transformation for training and testing data
    def initiate_data_transformation(self, train_path, test_path):   
        try:
            # Load training and testing data from CSV files
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Log that data has been read successfully
            logging.info("Read train and test data completed")

            # Obtain the preprocessor object
            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            # Define target column
            target_column_name = "math_score"
            # Numerical columns
            numerical_columns = ["writing_score", "reading_score"]

            # Split train data into input features and target variable
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)  # Drop target from train set
            target_feature_train_df = train_df[target_column_name]  # Isolate target column

            # Split test data similarly
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)  # Drop target from test set
            target_feature_test_df = test_df[target_column_name]  # Isolate target column

            # Log the application of the preprocessing object
            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

            # Apply the preprocessor to the training data (fit_transform to fit and transform at once)
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            """
            .fit_transform() method is called on preprocessing_obj, which is an instance of ColumnTransformer. 
            This method is available for pipeline-like objects, such as Pipeline and ColumnTransformer, because they are designed to 
            apply transformations to data in a sequential manner.
            """

            # Apply the preprocessor to the test data (only transform, since it's already fitted)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine the transformed input features with the target column for the train set
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            # Combine the transformed input features with the target column for the test set
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Log the successful saving of the preprocessor object
            logging.info("Saved preprocessing object.")

            # Save the preprocessor object (e.g., using pickle)
            """
            What is the need of saving preprocessor object as pickle file ? like model file.
            1. **Reusability**: Allows using the same preprocessor on new data without retraining preprocessor using fit.
2. **Consistency**: Ensures identical transformations across training and new datasets.
3. **Deployment**: Enables preprocessing new data in production exactly like training data.
4. **Time Efficiency**: Saves time by avoiding refitting the preprocessor for each use.
5. **Versioning and Reproducibility**: Tracks preprocessing versions for consistency and comparison.
            
            """
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Return the processed train and test data arrays, and the file path of the preprocessor object
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            # Raise a custom exception in case of an error
            raise CustomException(e, sys)
