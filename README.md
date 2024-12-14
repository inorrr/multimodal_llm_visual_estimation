# VisionClue

## Overview

VisionClue is a two-stage prompting strategy designed to improve the performance of multi-modal language models on object counting tasks in images. This repository contains the code and documentation used to implement VisionClue, which uses self-generated hints to enhance model accuracy without additional data requirements.

## Repository Structure

- `FSC147_384_V2/`: Scripts for preprocessing the FSC147 dataset.
- `plots/`: Contains visualization scripts that generate plots comparing model performance and object counts.
- `results/`: Directory for storing output files from the experiments.
- `helpers.py`: Utility functions used across different scripts.
- `human_evaluation_gui.py`: A GUI tool for manual object counting to compare against model performance.
- `preprocess_FSC147.py`: Preprocessing script for the FSC147 dataset.
- `rmse_evaluation.py`: Script to calculate the RMSE of model predictions against true values.
- `analysis_summary.py`: Summary script that compiles results from various experiments.
- `gpt4_evaluation.py`: Contains the implementation of the GPT-4 model evaluations with different prompting strategies.

## Human Evaluation Instructions

To assess human performance:
1. Execute `human_evaluation_gui.py` to start the manual counting process.
2. Results will be saved to `FSC147_384_V2/selected_300_image_annotation.csv` in the last column labeled "human".
3. A message "No more images to label." indicates the completion of all 300 image assessments.
