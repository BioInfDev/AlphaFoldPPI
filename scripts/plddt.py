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

y_plddt = np.array(data['atom_plddts'], dtype=float)
x_plddt = list(range(1, len(y_plddt) + 1))
chain_ids = data['atom_chain_ids']
bound = chain_ids.index('B')

# pLDDT plot
fig = go.Figure(go.Scatter(
    x=x_plddt,
    y=y_plddt,
    mode='lines',
    line=dict(width=0.5, color="#021120"),
    hovertemplate='plDDT: %{y:.1f}<br>Atom: %{x}<br><extra></extra>'
))

fig.add_shape(type='rect', x0=10, x1=x_plddt[-1], y0=0,  y1=50,  fillcolor='#d73027', line_width=0, layer='below')
fig.add_shape(type='rect', x0=10, x1=x_plddt[-1], y0=50, y1=70,  fillcolor='#fdae61', line_width=0, layer='below')
fig.add_shape(type='rect', x0=10, x1=x_plddt[-1], y0=70, y1=90,  fillcolor='#abd9e9', line_width=0, layer='below')
fig.add_shape(type='rect', x0=10, x1=x_plddt[-1], y0=90, y1=100, fillcolor='#2c7bb6', line_width=0, layer='below')
fig.add_shape(type='line', x0=bound, x1=bound, y0=0, y1=100, line=dict(color='black', width=1, dash='dash'))   

fig.update_layout(
    title=dict(text='Atom pLDDTs', x=0.5, xanchor='center'),
    xaxis_title='Atom',
    yaxis_title='pLDDT',
    width=1400,
    height=700,
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)
fig.write_html(f'{args.chain_a}_{args.chain_b}_pLDDT.html')