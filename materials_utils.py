import os
from mp_api.client import MPRester
from robocrys import StructureCondenser, StructureDescriber
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")


def get_mpid(formula):
    try:
        with MPRester(api_key) as mpr:
            docs = mpr.materials.summary.search(formula=[formula], fields=["material_id", "formula_pretty"])
            mpid_formula_dict = {doc.material_id: doc.formula_pretty for doc in docs}
        return mpid_formula_dict
    except Exception as e:
        st.write(f"Error finding MP data for formula {formula}: {e}")
        return None


def extract_data(doc, field_list):
    extracted_data = {}
    for field in field_list:
        if hasattr(doc, field):
            value = getattr(doc, field)
            extracted_data[field] = value
    return extracted_data


field_list = [
    'builder_meta', 'nsites', 'elements', 'nelements', 'composition',
    'composition_reduced', 'formula_pretty', 'formula_anonymous', 'chemsys',
    'volume', 'density', 'density_atomic', 'symmetry', 'property_name',
    'material_id', 'deprecated', 'deprecation_reasons', 'last_updated',
    'origins', 'warnings', 'structure', 'task_ids', 'uncorrected_energy_per_atom',
    'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull',
    'is_stable', 'equilibrium_reaction_energy_per_atom', 'decomposes_to',
    'xas', 'grain_boundaries', 'band_gap', 'cbm', 'vbm', 'efermi',
    'is_gap_direct', 'is_metal', 'es_source_calc_id', 'bandstructure', 'dos',
    'dos_energy_up', 'dos_energy_down', 'is_magnetic', 'ordering',
    'total_magnetization', 'total_magnetization_normalized_vol',
    'total_magnetization_normalized_formula_units', 'num_magnetic_sites',
    'num_unique_magnetic_sites', 'types_of_magnetic_species', 'bulk_modulus',
    'shear_modulus', 'universal_anisotropy', 'homogeneous_poisson', 'e_total',
    'e_ionic', 'e_electronic', 'n', 'e_ij_max', 'weighted_surface_energy_EV_PER_ANG2',
    'weighted_surface_energy', 'weighted_work_function', 'surface_anisotropy',
    'shape_factor', 'has_reconstructed', 'possible_species', 'has_props',
    'theoretical', 'database_IDs'
]


def get_data_from_mpid(mpid):
    with MPRester(api_key) as mpr:
        docs = mpr.materials.summary.search(material_ids=[mpid])
    if docs:
        data_dict = extract_data(docs[0], field_list)
        return data_dict
    else:
        return None


def get_structure_description(mpid):
    with MPRester(api_key) as mpr:
        structure = mpr.get_structure_by_material_id(mpid)
    condenser = StructureCondenser()
    describer = StructureDescriber()
    condensed_structure = condenser.condense_structure(structure)
    description = describer.describe(condensed_structure)
    return description
