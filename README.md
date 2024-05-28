# VIB Technical Interview Project

This repository was created for the technical interview for the Informatician position at VIB Discovery Sciences.

## Repository Contents

1. **compounds.csv**: This is the dataset that was provided for the project.
2. **VIB-DS_AI_ML_Challenge.pdf**: This PDF contains the description of the tasks that needed to be completed for the technical interview.
3. **similarity_functions.py**: This Python file contains all the functions necessary to compute the k most similar compound pairs.
4. **main.ipynb**: This is the main Jupyter Notebook that calculates the 10 most similar compound pairs.
5. **main_dash.ipynb**: Even though the main.ipynb implementation calculates the similarities in around 15 seconds on a MacBook Air, this notebook includes an implementation using Dask to parallelize the process at different stages of the pipeline. 
6. **streamlit_main.py**: A Streamlit app that allows users to compute the k most similar compound pairs via a graphical user interface.

## Instructions

1. **compounds.csv**: Ensure this dataset is in the root directory before running any scripts.
4. **main.ipynb**: Open and run this notebook to compute the 10 most similar compound pairs.
5. **main_dash.ipynb**: For a parallelized version using Dask, open and run this notebook.
6. **streamlit_main.py**: To use the Streamlit app, run `streamlit run streamlit_main.py` in your terminal and follow the instructions in the app.

## Requirements

Please ensure you have all necessary packages installed. You can install the required packages by running: `pip install -r requirements.txt`



