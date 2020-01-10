import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import copy
from collections import defaultdict
import sqlite3

# creates the duplicate index
def create_dupe_index(df, ind_name):
	df[ind_name+'_back'] = df[ind_name]
	return df

# renames old index dupe column in df and resets the index
def reset_dupe_index(df, ind_name):
	df.rename({ind_name: ind_name+'_back'}, inplace=True, axis=1)
	df.reset_index(inplace=True)
	return(df)

# set index, rename dupe index in df
def set_dupe_index(df, ind_name):
	df.set_index(ind_name, inplace=True)
	df.rename({ind_name+'_back': ind_name}, inplace=True, axis=1)
	return(df)

# partner function to label_edges
def set_edge_attrs(x, G, f_df, f_e):
	attr = {(x.v1, x.v2): {f_e: x[f_df]}}
	nx.set_edge_attributes(G, attr)
	return G

# label edges in G based on fields of edge_df
def label_edges(G, edge_df, f_df, f_e):
	edge_df.apply(lambda x: set_edge_attrs(x, G, f_df, f_e), axis=1)
	return G

# parter function to label_nodes
def set_node_attrs(x, G, f_df, f_n):
	attr = {x.vertex_id: {f_n: x[f_df]}}
	nx.set_node_attributes(G, attr)
	return G

# label nodes in G based on fields of loc_df
def label_nodes(G, loc_df, f_df, f_n):
	loc_df.apply(lambda x: set_node_attrs(x, G, f_df, f_n), axis=1)
	return G

# get value associated with keyword in the 9th column of gtf
def get_field_value(key, fields):
    if key not in fields:
        return None
    else:
        return fields.split(key+' "')[1].split()[0].replace('";','')

# creates a dictionary of the last field of a gtf
# adapted from Dana Wyman
def get_fields(fields):
    attributes = {}

    description = fields.strip()
    description = [x.strip() for x in description.split(";")]
    for pair in description:
        if pair == "": continue

        pair = pair.replace('"', '')
        key, val = pair.split()
        attributes[key] = val

    # put in placeholders for important attributes (such as gene_id) if they
    # are absent
    if "gene_id" not in attributes:
        attributes["gene_id"] = "NULL"

    return attributes    

# return a table indexed by transcript id with the appropriate 
# abundance
# currently only works with TALON abundance files but can easily 
# be updated to work with more types of abundance files
def process_abundance_file(file, cols):

	df = pd.read_csv(file, sep='\t')
	keep_cols = ['annot_transcript_id']+cols
	df = df[keep_cols]

	# get the counts
	df['counts'] = df.apply(lambda x: sum(x[cols]), axis=1)

	# get tpms
	for col in cols: 
		total_counts = df[col].sum()
		df['{}_tpm'.format(col)] = df.apply(lambda x: (x[col]*1000000)/total_counts, axis=1)
	cols = ['{}_tpm'.format(col) for col in cols]
	df['tpm'] = df[cols].mean(axis=1)

	# set up for merging
	df.drop(cols, axis=1, inplace=True)
	df.rename({'annot_transcript_id': 'tid'}, inplace=True, axis=1)
	return df

# creates a file name based on input plotting arguments
def create_fname(prefix, combine, indicate_dataset,
				 indicate_novel, browser,
				 ftype='figure', tid=None, gid=None):
	fname = prefix
	if combine:
		fname += '_combine'
	if indicate_dataset:
		fname += '_{}'.format(indicate_dataset)
	if indicate_novel:
		fname += '_novel'
	if browser: 
		fname += '_browser'
	if tid: 
		fname += '_{}'.format(tid)
	if gid: 
		fname += '_{}'.format(gid)
	if ftype == 'figure':
		fname += '.png'
	elif ftype == 'report':
		fname += '_report.pdf'
	return fname


	





