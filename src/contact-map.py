#!/usr/bin/env python3
import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from Bio.PDB import MMCIFParser
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN


p = argparse.ArgumentParser()
p.add_argument('cif', type=Path)
p.add_argument('-c1', '--chain-a', type=str, default='A')
p.add_argument('-c2', '--chain-b', type=str, default='B')
p.add_argument('-t', '--threshold', type=float, default=8.0)
args = p.parse_args()

# Read CIF
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure('AF-COMPLEX', Path(args.cif).resolve())

# Selection of model and chains
model = structure[0]
chain_A = model['A']
chain_B = model['B']

# Extraction of atoms, their coordinates, and residues
atoms_A = [a for a in chain_A.get_atoms() if a.element]
atoms_B = [a for a in chain_B.get_atoms() if a.element]

coords_A = np.array([a.get_coord() for a in atoms_A])
coords_B = np.array([a.get_coord() for a in atoms_B])
res_A = np.array([a.get_parent().get_id()[1] for a in atoms_A])
res_B = np.array([a.get_parent().get_id()[1] for a in atoms_B])

# Calculation of the distance matrix
dist_matrix = cdist(coords_A, coords_B)

# Search for contacts
contact_pairs = np.where(dist_matrix <= args.threshold)
point_contacts = np.array(sorted({(res_A[i], res_B[j]) for i, j in zip(*contact_pairs)}), dtype=float).reshape(-1, 2)

if len(point_contacts) == 0:
    labels = np.empty(0, dtype=int)
else:
    labels = DBSCAN(eps=50, min_samples=1).fit_predict(point_contacts)

groups = defaultdict(list)
for (a, b), lab in zip(point_contacts.astype(int), labels):
    groups[lab].append((a, b))

contacts = pd.DataFrame(
    [
        {
            "Contact": cid,
            args.chain_a: f'{min(p[0] for p in pts)}-{max(p[0] for p in pts)}',
            args.chain_b: f'{min(p[1] for p in pts)}-{max(p[1] for p in pts)}'
        }
        for cid, pts in sorted(groups.items())
    ],
    columns=["Contact", args.chain_a, args.chain_b]
)
contacts.to_csv(args.chain_a + '_' + args.chain_b + '_CONTACT_MAP_CONTACTS.csv', index = False)

# Contact map
fig = go.Figure(go.Scatter(
    x=point_contacts[:, 0],
    y=point_contacts[:, 1],
    mode='markers',
    marker=dict(
        size=7,
        color=labels,
        colorscale='Turbo',
        showscale=False,
        line=dict(width=0.5, color='white')
    ),
    customdata=labels,
    hovertemplate=f'{args.chain_a}: %{{x}}<br>{args.chain_b}: %{{y}}<br>Cluster: %{{customdata}}<extra></extra>'
))
fig.update_layout(
    title=f'{args.chain_a} – {args.chain_b}: Inter-Chain Contact Map (d ≤ {args.threshold} Å)',
    xaxis_title=args.chain_a,
    yaxis_title=args.chain_b,
    xaxis=dict(range=[-10, max(res_A) + 10]),
    yaxis=dict(range=[-10, max(res_B) + 10]),
    template='plotly_white'
)
fig.write_html(f'{args.chain_a}_{args.chain_b}_CONTACT_MAP.html')