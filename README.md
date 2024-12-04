# VisionClue

This is the complete repository for the project: **Improving Multi-modal Language Model on Object Counting with Self-Generated Side Information**.



## TODO List:
1. **DONE:** Set up repository.
2. **DONE:** Preprocess the dataset: 
    - **DONE:** select 300 images
    - **DONE:** extract the true count from annotion json -> len(annotations[filename]['points'])
3. **WORKING:** Human accuracy
4. **DONE:** gpt4: 
    - **DONE:** gpt4 initial prediction.
    - **DONE:** gpt4 hints: description, direct hint, indirect hint
        - **WORKING:** split the hints to three entries
    - gpt4 prediction with hint:
        - Description only
        - direct hint only
        - indirect hint only
        - all three
4. CLIP: 
    - CLIP initial prediction.
    - CLIP hints: description, direct hint, indirect hint
        - split the hints to three entries
    - CLIP prediction with hint:
        - Description only
        - direct hint only
        - indirect hint only
        - all three
5. Performance Analysis
    - Figures and Tables
6. Report
    - Written Part
    - Figues



## Instruction to do human evaluation
Human performance: run `human_evaluation_gui.py` and start counting. 
1. Result will be saved to `FSC147_384_V2/selected_300_image_annotation.csv`, last column "human".
2. Seeing "No more images to label." means that we have finished all 300 images!!

## Files
1. `FSC147_384_V2/selected_300_images` : the 300 images to be use for this stdy.
2. `FSC147_384_V2/selected_300_image_annotation.csv`: contains file name, object name, and the ground truth count, human count is also stored in here.
3. `results/gpt4_evaluation.csv` all gpt results.
4. `helpers.py` helper functions to encode images and generate prompts.