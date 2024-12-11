"""
Date: Dec 3, 2024
Author: Yuanyi (Leo) Liu
Project: Improving Multi-modal Language Model on Object Counting with Self-Generated Side Information
"""

import pandas as pd
import numpy as np


def calculate_rmse(df, correct_counts_column, method_column):
    """
    Calculates RMSE for a specific method (e.g., GPT initial, GPT all hints).

    Parameters:
    df (DataFrame): The DataFrame containing the data.
    correct_counts_column (str): The column name containing the correct object counts.
    method_column (str): The column name containing the method's predicted counts.

    Returns:
    float: The RMSE value for the specified method.
    """
    correct_counts = df[correct_counts_column]
    method_counts = df[method_column]
    return np.sqrt(((correct_counts - method_counts) ** 2).mean())


def calculate_rmse_for_ranges(df, correct_counts_column, method_column=None):
    """
    Calculates RMSE for different object count ranges from the DataFrame.

    Parameters:
    df (DataFrame): The DataFrame containing human or GPT counts.
    correct_counts_column (str): The column name containing the correct object counts.
    method_column (str): Optional; the method column to calculate RMSE for specific methods.

    Returns:
    dict: A dictionary with RMSE values for each range and overall performance.
    """
    rmse_results = {}
    conditions = [
        (df[correct_counts_column] < 20),
        (df[correct_counts_column] >= 20) & (df[correct_counts_column] < 100),
        (df[correct_counts_column] >= 100)
    ]
    range_labels = ['Count < 20 performance', '20 <= Count < 100 performance', 'Count >= 100 performance']

    for i, condition in enumerate(conditions):
        range_data = df[condition]
        rmse_results[range_labels[i]] = calculate_rmse(range_data, correct_counts_column, method_column)

    # Overall performance
    rmse_results['Overall performance'] = calculate_rmse(df, correct_counts_column, method_column)

    # Count of NAs
    rmse_results['Number of NA (cannot count)'] = df[method_column].isna().sum() if method_column else 0

    return rmse_results


def update_rmse_in_output_file(output_file, rmse_results):
    """
    Updates the output CSV file with RMSE values for each method and range.

    Parameters:
    output_file (str): Path to the CSV file to read and update.
    rmse_results (dict): The RMSE values for each method and range.
    """
    df_results = pd.read_csv(output_file)

    # Update RMSE values in output file for each method
    for method, rmse_ranges in rmse_results.items():
        for range_label, rmse in rmse_ranges.items():
            df_results.loc[df_results['Method'] == method, range_label] = rmse

    df_results.to_csv(output_file, index=False)
    print(f"Updated the output file with RMSE values: {rmse_results}")


def process_human_and_gpt_rmse(human_file, gpt4_file, output_file):
    """
    Calculates and updates RMSE for both human and GPT methods in the output file.

    Parameters:
    human_file (str): Path to the CSV file with human evaluation data.
    gpt4_file (str): Path to the CSV file with GPT evaluation data.
    output_file (str): Path to the CSV file to update.
    """
    # Calculate and update RMSE for human
    human_df = pd.read_csv(human_file)
    human_rmse_results = calculate_rmse_for_ranges(human_df, 'object_count', 'human')
    update_rmse_in_output_file(output_file, {'Human': human_rmse_results})

    # Calculate and update RMSE for GPT methods
    gpt4_df = pd.read_csv(gpt4_file)
    gpt_methods = {
        'GPT initial': 'gpt_4_initial_answer',
        'GPT all hints': 'response_desc_true_direct_true_indirect_true',
        'GPT description': 'response_desc_true_direct_false_indirect_false',
        'GPT direct': 'response_desc_false_direct_true_indirect_false',
        'GPT indirect': 'response_desc_false_direct_false_indirect_true'
    }

    gpt_rmse_results = {}
    for method, column in gpt_methods.items():
        gpt_rmse_results[method] = calculate_rmse_for_ranges(gpt4_df, 'object_count', column)

    update_rmse_in_output_file(output_file, gpt_rmse_results)


if __name__ == "__main__":
    human_file = "results/human_evaluation.csv"
    gpt4_file = "results/gpt4_evaluation.csv"
    output_file = "results/rmse_evaluation.csv"

    process_human_and_gpt_rmse(human_file, gpt4_file, output_file)
