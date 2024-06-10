import os
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import AllChem
import plotly.graph_objects as go
import streamlit as st
import numpy as np


def get_chemical_name(formula):
    try:
        comp = pcp.get_compounds(formula, 'formula')
        if comp:
            return comp[0].iupac_name
        else:
            return None
    except Exception as e:
        st.write(f"Error finding chemical name for formula {formula}: {e}")
        return None


def visualize_molecule(smiles):
    molecule = Chem.MolFromSmiles(smiles)
    molecule = Chem.AddHs(molecule)
    AllChem.EmbedMolecule(molecule, randomSeed=42)
    AllChem.UFFOptimizeMolecule(molecule)
    conf = molecule.GetConformer()

    atom_coords = []
    atom_types = []
    for atom in molecule.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        atom_coords.append((pos.x, pos.y, pos.z))
        atom_types.append(atom.GetSymbol())

    atom_coords = np.array(atom_coords)

    bonds = []
    for bond in molecule.GetBonds():
        start = bond.GetBeginAtomIdx()
        end = bond.GetEndAtomIdx()
        bonds.append((start, end))

    fig = go.Figure()

    for i, (x, y, z) in enumerate(atom_coords):
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers',
            marker=dict(size=10, color='red'),
            text=atom_types[i],
            hoverinfo='text'
        ))

    for bond in bonds:
        start, end = bond
        xs = [atom_coords[start][0], atom_coords[end][0]]
        ys = [atom_coords[start][1], atom_coords[end][1]]
        zs = [atom_coords[start][2], atom_coords[end][2]]
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines',
            line=dict(color='blue', width=4)
        ))

    fig.update_layout(title='3D Structure', showlegend=False)
    st.plotly_chart(fig)
