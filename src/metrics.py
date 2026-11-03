#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import pandas as pd
from af_analysis import Data, analysis, docking


p = argparse.ArgumentParser()
p.add_argument('fold', type=Path)
p.add_argument('-c1', '--chain-a', type=str, default='A')
p.add_argument('-c2', '--chain-b', type=str, default='B')
args = p.parse_args()


# Interface metrics
AF_ANAL_DATA = Data(args.fold)
analysis.pdockq(AF_ANAL_DATA)
analysis.pdockq2(AF_ANAL_DATA)
analysis.ipSAE(AF_ANAL_DATA)
docking.LIS_pep(AF_ANAL_DATA)

# All metrics
for i in range(5):
    AF_ANAL_ROW = AF_ANAL_DATA.df.iloc[i]
    with open(args.fold / f'{args.fold.stem}_summary_confidences_{i}.json', 'rt') as f:
        fold_data = json.load(f)

    structure_metrics = {
        'pTM': fold_data['ptm'],
        'ipTM': fold_data['iptm'],
        'Has clash': fold_data['has_clash'],
        'Fraction disordered': fold_data['fraction_disordered'],
        'Ranking score': fold_data['ranking_score']
    }

    interaction_metrics = {
        f'Chain pair [{args.chain_a}-{args.chain_b}] min(PAE)': fold_data['chain_pair_pae_min'][0][1],
        f'Chain pair [{args.chain_b}-{args.chain_a}] min(PAE)': fold_data['chain_pair_pae_min'][1][0],
        f'Chain pair [{args.chain_a}-{args.chain_b}] ipTM': fold_data['chain_pair_iptm'][0][1],
        f'Chain pair [{args.chain_b}-{args.chain_a}]] ipTM': fold_data['chain_pair_iptm'][1][0],
        f'pDockQ': AF_ANAL_ROW['pdockq'],
        f'pDockQ2 [{args.chain_a}-{args.chain_b}]': AF_ANAL_ROW['pdockq2_A'],
        f'pDockQ2 [{args.chain_b}-{args.chain_a}]': AF_ANAL_ROW['pdockq2_B'],
        f'LIS [{args.chain_a}-{args.chain_b}]': AF_ANAL_ROW['LIS'][0][1],
        f'LIS [{args.chain_b}-{args.chain_a}]': AF_ANAL_ROW['LIS'][1][0],
    }

    df_summary = pd.DataFrame([structure_metrics]).to_csv(f'{args.chain_a}_{args.chain_b}_structure_metrics_model_{i}.csv', index=False)
    df_summary = pd.DataFrame([interaction_metrics]).to_csv(f'{args.chain_a}_{args.chain_b}_interaction_metrics_model_{i}.csv', index=False)