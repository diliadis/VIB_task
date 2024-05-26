import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs, Draw
import itertools
from tqdm import tqdm
# import matplotlib.pyplot as plt
# import seaborn as sns

def read_data_from_csv(file_path):
    """
    Read SMILES strings and ChEMBL IDs from a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: A DataFrame containing the SMILES strings and ChEMBL IDs.
    """
    df = pd.read_csv(file_path)
    return df

def calculate_fingerprints(df, smiles_column='canonical_smiles'):
    """
    Calculate molecular fingerprints for SMILES strings and add them to the DataFrame.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing the SMILES strings and ChEMBL IDs.
    smiles_column (str): The name of the column containing the SMILES strings. Default is 'canonical_smiles'.
    
    Returns:
    pd.DataFrame: The input DataFrame with additional columns for molecular fingerprints.
    """
    def fingerprint_from_smiles(smiles, smiles_column='canonical_smiles'):
        return AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(smiles), 2, nBits=2048)

    df['fingerprint'] = df['canonical_smiles'].apply(fingerprint_from_smiles)
    return df

def calculate_pairwise_similarities(df, similarity_function=DataStructs.TanimotoSimilarity):
    """
    Calculate pairwise similarities between molecular fingerprints.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing the molecular fingerprints.
    similarity_function (function): A function that calculates the similarity between two fingerprints.
    
    Returns:
    list: A list of tuples where each tuple contains a pair of indices and their similarity score.
    """
    similarities = []
    pairs = list(itertools.combinations(enumerate(df['fingerprint']), 2))
    for (i, fp1), (j, fp2) in tqdm(pairs, desc="Calculating similarities"):
        if fp1 is not None and fp2 is not None:
            similarity = similarity_function(fp1, fp2)
            similarities.append(((i, j), similarity))
    return similarities

def find_top_n_similarities(similarities, df, n=10):
    """
    Find the top N similarities and return the ChEMBL IDs along with similarity scores.
    
    Parameters:
    similarities (list): A list of tuples containing pairs of indices and their similarity scores.
    df (pd.DataFrame): A DataFrame containing the SMILES strings and ChEMBL IDs.
    n (int): The number of top similarities to return. Default is 10.
    
    Returns:
    list: A list of tuples where each tuple contains ChEMBL IDs, canonical smiles and their similarity score.
    """
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similarities = similarities[:n]
    top_pairs_with_ids = [
        ((df.iloc[pair[0]]['chembl_id'], df.iloc[pair[1]]['chembl_id']),
         (df.iloc[pair[0]]['canonical_smiles'], df.iloc[pair[1]]['canonical_smiles']),
         similarity)
        for pair, similarity in top_similarities
    ]
    return top_pairs_with_ids

def smiles_to_image(smiles, size=(500, 500)):
    """
    Convert a SMILES string to a molecular image.

    Parameters:
    smiles (str): The SMILES string representing the molecule.
    size (tuple): The size of the generated image in pixels (width, height). Default is (300, 300).

    Returns:
    PIL.Image: An image of the molecule.
    """
    mol = Chem.MolFromSmiles(smiles)
    img = Draw.MolToImage(mol, size=size)
    return img