import streamlit as st
import pandas as pd
from rdkit.Chem import DataStructs
import similarity_functions as sf
# import plotly.express as px

st.title("Molecular Similarity Calculator")

st.sidebar.header("User Inputs")
st.logo("VIB_logo.png", icon_image="VIB_logo.png")

# Define a form in the sidebar
with st.sidebar.form("input_form"):
    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

    # Fingerprint type selection
    fingerprint_type = st.selectbox("Select fingerprint type", options=['Morgan'])

    # Similarity function selection
    similarity_function_name = st.selectbox("Select similarity function", options=['Tanimoto', 'Dice'])

    # Number of top similarities
    top_n = st.number_input("Number of top similarities", min_value=1, max_value=100, value=10)

    # Submit button for the form
    submit_button = st.form_submit_button(label="Submit")

if similarity_function_name == 'Tanimoto':
    similarity_function = DataStructs.TanimotoSimilarity
elif similarity_function_name == 'Dice':
    similarity_function = DataStructs.DiceSimilarity

if submit_button and uploaded_file is not None:
    with st.status("Processing..."):
        # Step 1: Read SMILES strings from the uploaded CSV file
        st.write("Reading .csv...")
        df = sf.read_data_from_csv(uploaded_file)

        # Step 2: Calculate fingerprints for each SMILES string within the DataFrame
        st.write("Calculating fingerprints for every compound in the dataset...")
        df = sf.calculate_fingerprints(df)

        # Step 3: Calculate pairwise similarities
        st.write('Calculating pairwise similarities...')
        similarities = sf.calculate_pairwise_similarities(df, similarity_function)

        # Step 4: Find the top N similarities
        st.write('Sorting pairwise similarities...')
        top_similarities = sf.find_top_n_similarities(similarities, df, n=top_n)

    # Display results
    st.header("Top Similarities:")
    for i, (ids, smiles, similarity) in enumerate(top_similarities):
        img1 = sf.smiles_to_image(smiles[0])
        img2 = sf.smiles_to_image(smiles[1])
        st.subheader(f"{i + 1})")
        col1, col2 = st.columns(2)
        with col1:
            st.image(img1, caption=f"{ids[0]}")
        with col2:
            st.image(img2, caption=f"{ids[1]}")
        
        col1, col2, col3 = st.columns(3)
        col2.subheader(f"Similarity: {round(similarity, 4)}")
        st.divider()
        
    # # Add a histogram of the similarities
    # st.header("Histogram of Similarities")
    # similarity_scores = [similarity for _, similarity in similarities]
    # fig = px.histogram(similarity_scores, nbins=100, title='Distribution of Top Similarities',
    #                    labels={'value':'Similarity Score', 'count':'Frequency'})
    # st.plotly_chart(fig)

else:
    st.write("Please upload a CSV file to proceed.")