from pathlib import Path

import argparse
import pandas as pd
from jinja2 import Template


p = argparse.ArgumentParser()
p.add_argument('output', type=Path)
p.add_argument('-c1', '--chain-a', type=str, default='A')
p.add_argument('-c2', '--chain-b', type=str, default='B')
args = p.parse_args()


MODEL_OUTPUT = args.output
SCRIPT_DIR = Path(__file__).parent
REPORT_TEMPLATE = Template((SCRIPT_DIR / 'template.html').read_text(encoding="utf-8"))

chain_render = next(MODEL_OUTPUT.glob('*_chain_render.html')).read_text(encoding='utf-8')
pae = next(MODEL_OUTPUT.glob('*_PAE.html')).read_text(encoding="utf-8")
contact_map = next(MODEL_OUTPUT.glob('*_CONTACT_MAP.html')).read_text(encoding="utf-8")

structure_metrics = pd.read_csv(next(MODEL_OUTPUT.glob('*_structure_metrics_*'))).to_html(index=False, classes='my-table', border=0, escape=False)
interaction_metrics = pd.read_csv(next(MODEL_OUTPUT.glob('*_interaction_metrics_*'))).to_html(index=False, classes='my-table', border=0, escape=False)
contacts = pd.read_csv(next(MODEL_OUTPUT.glob('*CONTACT_MAP_CONTACTS.csv'))).to_html(index=False, classes='my-table', border=0, escape=False)

output_html = REPORT_TEMPLATE.render(complex=f'{args.chain_a}-{args.chain_b}', chain_render=chain_render, pae=pae, structure_metrics=structure_metrics, interaction_metrics=interaction_metrics, contact_map=contact_map, contacts=contacts)

Path('REPORT.html').write_text(output_html, encoding="utf-8")