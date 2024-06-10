import streamlit as st
from chemical_utils import get_chemical_name, visualize_molecule
from materials_utils import get_mpid, get_data_from_mpid, get_structure_description
from visualization_utils import display_data_table
import pubchempy as pcp

st.title("Materials and Chemical Data Retrieval")
st.text("This app retrieves data from the Materials Project API and PubChemPy API.")

if "step" not in st.session_state:
    st.session_state["step"] = 1

if st.session_state["step"] == 1:
    st.header("Step 1: Enter Chemical Formula")
    chemical = st.text_input("Enter a chemical formula:", "Fe2O3")
    if st.button("Get MP IDs"):
        mpid_dict = get_mpid(chemical)
        if mpid_dict:
            st.session_state["mpid_dict"] = mpid_dict
            st.session_state["chemical"] = chemical
            st.session_state["step"] = 2
        else:
            st.write("No MP IDs found for this formula.")

elif st.session_state["step"] == 2:
    st.header("Step 2: Select MP ID")
    chemical = st.session_state["chemical"]
    mpid_dict = st.session_state["mpid_dict"]
    mpid = st.selectbox("Select an MP ID:", list(mpid_dict.keys()))
    if st.button("Get Data"):
        st.write(f"Material ID: {mpid}")
        data_dict = get_data_from_mpid(mpid)
        if data_dict:
            # available_fields = list(data_dict.keys())
            # selected_fields = st.multiselect("Select fields to display:", available_fields, default=available_fields)
            # display_data_table(data_dict, selected_fields)
            st.write("Structure Description:")
            description = get_structure_description(mpid)
            st.write(description)
        else:
            st.write("No data found for this material ID.")

    chemical_name = get_chemical_name(chemical)
    if chemical_name:
        st.write(f"Chemical Name: {chemical_name}")
        try:
            compounds = pcp.get_compounds(chemical_name, 'name')
            if compounds:
                smiles = compounds[0].isomeric_smiles
                st.write("3D Structure:")
                visualize_molecule(smiles)
            else:
                st.write("No 3D structure found for this formula.")
        except Exception as e:
            st.write(f"Error retrieving 3D structure: {e}")
    else:
        st.write("No chemical name found for this formula.")

if st.button("Start Over"):
    st.session_state["step"] = 1
