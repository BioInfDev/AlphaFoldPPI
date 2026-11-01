#!/usr/bin/env python3
from pathlib import Path

import argparse
import py3Dmol


def render(view, legend):
    return f"""
            <!DOCTYPE html>
            <html>
            <body
                <div style="display: flex; flex-direction: column; align-items: center; padding: 20px 0;">
                    {view}{legend}
                </div>
            </body>
            </html>
            """

p = argparse.ArgumentParser()
p.add_argument('file', type = Path)
p.add_argument('-c1', '--chain-a', type = str, default = 'A')
p.add_argument('-c2', '--chain-b', type = str, default = 'B')
args = p.parse_args()

SETTINGS = {
    'mmCIF': Path(args.file),
    'WIDTH': 1600,
    'HEIGHT': 800,
    'COLOR_A': '#4682B4',
    'COLOR_B': '#FF7F50',
    'OUTPUT_PREFIX': args.chain_a + '_' + args.chain_b
}

# Read CIF
with open(SETTINGS['mmCIF'], 'r', encoding = 'utf-8') as f:
    raw_cif = f.read()

# Chain View
chain_view = py3Dmol.view(width = SETTINGS['WIDTH'], height = SETTINGS['HEIGHT'])
chain_view.addModel(raw_cif, 'cif')

chain_view.setStyle({'chain': 'A'},{'cartoon': {'color': SETTINGS['COLOR_A']}})
chain_view.setStyle({'chain': 'B'}, {'cartoon': {'color': SETTINGS['COLOR_B']}})
chain_view.zoomTo()

chain_legend = f"""
<div style="display: flex; justify-content: center; gap: 30px; font-family: sans-serif;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 20px; height: 20px; background-color: {SETTINGS['COLOR_A']}; border-radius: 6px;"></span>
        <span>{args.chain_a}</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 20px; height: 20px; background-color: {SETTINGS['COLOR_B']}; border-radius: 6px;"></span>
        <span>{args.chain_b}</span>
    </div>
</div>
"""
html_view = chain_view._make_html()

with open(SETTINGS['OUTPUT_PREFIX'] + '_chain_render.html', 'w', encoding = 'utf-8') as f:
    f.write(render(html_view, chain_legend))

# pLDDT View
plddt_view = py3Dmol.view(width=SETTINGS['WIDTH'], height=SETTINGS['HEIGHT'])
plddt_view.addModel(raw_cif, 'cif')
plddt_view.setStyle({'cartoon': {
    'colorscheme': {
        'prop': 'b',
        'gradient': 'roygb',
        'min': 50,
        'max': 90
    }
}})
plddt_view.zoomTo()

plddt_legend = f"""
<div style="display: flex; justify-content: center; width: 100%;">
    <div style="width: 100%; max-width: {SETTINGS['HEIGHT']}px; font-family: sans-serif;">
        <div style="display: flex; gap: 2px;">
            <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                <div style="width: 100%; height: 32px; background-color: #d73027; border-radius: 16px 0 0 16px;"></div>
                <div style="font-family: sans-serif; font-size: 12px; text-align: center; color: #333;">
                    <strong>Very low</strong><br><span style="color: #666;">0-50</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                <div style="width: 100%; height: 32px; background-color: #fdae61;"></div>
                <div style="font-family: sans-serif; font-size: 12px; text-align: center; color: #333;">
                    <strong>Low</strong><br><span style="color: #666;">50-70</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                <div style="width: 100%; height: 32px; background-color: #abd9e9;"></div>
                <div style="font-family: sans-serif; font-size: 12px; text-align: center; color: #333;">
                    <strong>Confident</strong><br><span style="color: #666;">70-90</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                <div style="width: 100%; height: 32px; background-color: #2c7bb6; border-radius: 0 16px 16px 0;"></div>
                <div style="font-family: sans-serif; font-size: 12px; text-align: center; color: #333;">
                    <strong>Very high</strong><br><span style="color: #666;">90-100</span>
                </div>
            </div>
        </div>
    </div>
</div>
"""

html_view = plddt_view._make_html()
with open(SETTINGS['OUTPUT_PREFIX'] + '_plddt_render.html', 'w', encoding = 'utf-8') as f:
    f.write(render(html_view, plddt_legend))