# ========== (c) JP Hwang 13/5/20  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

import pandas as pd
import numpy as np

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

# ===== LOAD & PROCESS POPULATION DATA =====
pop_df = pd.read_csv('srcdata/PopulationEstimates.csv', encoding='latin1')
pop_df = pop_df[pop_df['FIPS'].notna()]
pop_df['fips'] = pop_df.FIPS.astype(int)
pop_keys = ['fips', 'State', 'Area_Name', 'Rural-urban_Continuum Code_2013', 'Urban_Influence_Code_2013', 'POP_ESTIMATE_2018']
pop_df = pop_df[pop_keys]

# Clean data
pop_df['POP_ESTIMATE_2018'] = pop_df['POP_ESTIMATE_2018'].fillna('0').str.replace('[$,]', '', regex=True).astype(int)

# ===== LOAD & PROCESS POVERTY DATA =====
pov_df = pd.read_csv('srcdata/PovertyEstimates.csv', encoding='latin1')
pov_df = pov_df[pov_df['FIPStxt'].notna()]
pov_df['fips'] = pov_df.FIPStxt.astype(int)
pov_keys = ['fips', 'Area_name', 'PCTPOVALL_2018']
pov_df = pov_df[pov_keys]

# ===== LOAD & PROCESS EMPLOYMENT DATA =====
emp_df = pd.read_csv('srcdata/Unemployment.csv', encoding='latin1')
emp_df = emp_df[emp_df['FIPS'].notna()]
emp_df['fips'] = emp_df.FIPS.astype(int)
emp_keys = ['fips', 'State', 'Area_name', 'Unemployment_rate_2018', 'Median_Household_Income_2018']
emp_df = emp_df[emp_keys]

# Clean data
emp_df['Median_Household_Income_2018'] = emp_df['Median_Household_Income_2018'].fillna('0').str.replace('[$,]', '', regex=True).astype(int)

# ===== LOAD & PROCESS DEMOGRAPHIC DATA =====
demo_df = pd.read_csv('srcdata/cc-est2019-alldata.csv', encoding='latin1')
