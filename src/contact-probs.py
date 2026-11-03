#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go


p = argparse.ArgumentParser()
p.add_argument('json', type=Path)
p.add_argument('-c1', '--chain-a', type=str, default='A')
p.add_argument('-c2', '--chain-b', type=str, default='B')
args = p.parse_args()

# Read data
with open(args.json, 'rt') as f:
    data = json.load(f)

contact_probs = np.array(data['contact_probs'], dtype=float)
chain_ids = data['token_chain_ids']
bound = chain_ids.index('B')

# PAE plot
fig = go.Figure(go.Heatmap(
    z=contact_probs,
    colorscale='Greens_r',
    zmin=0,
    zmax=contact_probs.max(), 
    colorbar=dict(orientation='h', y=-0.25, thickness=15),
    hovertemplate='Aligned: %{y}<br>Scored: %{x}<br>Probability: %{z:.1f}<extra></extra>'
))

fig.add_shape(type='line', x0=bound, x1=bound, y0=0, y1=len(chain_ids), line=dict(color='black', width=1.5, dash='dash'))   
fig.add_shape(type='line', x0=0, x1=len(chain_ids), y0=bound, y1=bound, line=dict(color='black', width=1.5, dash='dash'))

fig.update_layout(
    title=dict(text='Contact probabilities Matrix', x=0.5, xanchor='center'),
    xaxis_title='Scored residue',
    yaxis_title='Aligned residue',
    yaxis_autorange='reversed',
    width=600,
    height=600,
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)
fig.write_html(f'{args.chain_a}_{args.chain_b}_contact_probs.html')