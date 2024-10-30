# An Exploration of Analysis Methods on Predictive Models of Student Success

This project explores machine learning models that predict student success in online courses, using a dataset from the Open University. Specifically, it compares traditional and Bayesian methods for model evaluation and introduces a fairness metric, Absolute Between Receiver Operating Characteristic Area (ABROCA), which assesses the model’s predictions across demographic subgroups.

## Overview

The primary goal is to predict students at risk of failing or withdrawing within the first 30 days of a course. Predictions like these could help guide resource allocation toward at-risk students.

The project includes:

1. **Data Engineering and Preprocessing**:  
   - The Open University Learning Analytics Dataset (OULAD) was imported into a PostgreSQL database for efficient data wrangling and cleansing.
   - Feature engineering created additional predictive fields from student demographics, course information, assessment data, and interactions with the virtual learning environment (VLE).

2. **Model Training and Evaluation**:  
   - Various machine learning classifiers, including tree-based ensemble methods, logistic regression, and support vector machines, were trained.
   - Hyperparameter tuning was conducted using both grid search and random search for optimized model performance.
   - Model performance was compared using frequentist and Bayesian evaluation techniques.

3. **Fairness Metric**:  
   - The ABROCA metric was applied to evaluate model fairness across gender and disability subgroups, showing correlations with demographic balance but little relationship with overall model performance.

## Repository Contents

This repository contains:

- **Data Processing Pipeline**: Scripts for setting up the database, loading the OULAD dataset, and transforming it into usable formats are located in `/src/app/etl/`.
- **Feature Engineering Scripts**: Custom scripts for creating predictive features based on student engagement and assessment data.
- **Model Training Pipeline**: A configurable pipeline using `scikit-learn` to train and test various classification models with exhaustive hyperparameter tuning can be found in `/src/app/model/main.py`.
- **Evaluation Metrics**: Implementations of frequentist tests (Friedman and Nemenyi) and Bayesian methods to compare model efficacy.
- **Fairness Analysis**: Code for calculating ABROCA and visualizing results across demographic categories is provided in the `/src/notebooks/ModelEvaluation.ipynb` notebook.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/witzbeck/master_proj.git
    cd master_proj
    ```

2. Install dependencies using [Poetry](https://python-poetry.org/):
    ```bash
    poetry install
    ```

3. Set up PostgreSQL for the data pipeline as per the instructions in the `/src/app/etl/` directory.

## Usage

- **Data Pipeline**: Run the ETL pipeline located in the `/src/app/etl/` directory to ingest, clean, and transform the dataset.
- **Model Training**: Use the model training pipeline in `/src/app/model/main.py` to train and evaluate models with specified hyperparameters.
- **Fairness Analysis**: Run the notebook `/src/notebooks/ModelEvaluation.ipynb` to calculate ABROCA and evaluate fairness across demographic groups.

## Results Summary

- **Best Performing Models**: Tree-based ensemble methods, such as Random Forest and Extra Trees, had the best overall performance.
- **Fairness Metric**: The ABROCA metric showed a strong association with demographic ratios but did not correlate directly with predictive accuracy, indicating that it may be a valuable fairness measure independent of performance.

## Future Work

Future development could expand on feature engineering, automate hyperparameter optimization, and further explore the fairness metric with additional datasets and subgroups.

## References

For a detailed explanation of the project’s methodology, please refer to [paper.pdf](https://github.com/witzbeck/master_proj/releases) in the latest release.
