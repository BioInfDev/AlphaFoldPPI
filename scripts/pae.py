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

pae = np.array(data['pae'], dtype=float)
chain_ids = data['token_chain_ids']
bound = chain_ids.index('B')

# PAE plot
fig = go.Figure(go.Heatmap(
    z=pae,
    colorscale='Greens_r',
    zmin=0,
    zmax=pae.max(), 
    colorbar=dict(orientation='h', y=-0.25, thickness=15),
    hovertemplate='Aligned: %{y}<br>Scored: %{x}<br>PAE: %{z:.1f} Å<extra></extra>'
))

fig.add_shape(type='line', x0=bound, x1=bound, y0=0, y1=len(chain_ids), line=dict(color='black', width=1.5, dash='dash'))   
fig.add_shape(type='line', x0=0, x1=len(chain_ids), y0=bound, y1=bound, line=dict(color='black', width=1.5, dash='dash'))

fig.update_layout(
    title=dict(text='PAE Matrix', x=0.5, xanchor='center'),
    xaxis_title='Scored residue',
    yaxis_title='Aligned residue',
    yaxis_autorange='reversed',
    width=700,
    height=700,
    template='plotly_white',
    plot_bgcolor='white',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)
fig.write_html(f'{args.chain_a}_{args.chain_b}_PAE.html')