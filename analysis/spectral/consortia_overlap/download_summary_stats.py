import multiprocessing as mp
import pandas as pd
from os import system,

def get_vcf(gwas_id):
    url = f'https://gwas.mrcieu.ac.uk/files/{gwas_id}/{gwas_id}.vcf.gz'
    system(f'wget {url}')


if __name__ == '__main__':

    gwas = pd.read_csv('gwas_for_LDSc_reg.csv')

    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(get_vcf, gwas.id.values)

    for i, row in gwas.iterrows():
        vcf_file = f'{row.id}.vcf.gz'
        consort_str = row.consortium.replace(" ", "_")
        system(f'mv {vcf_file} vcfs/{consort_str}_{vcf_file}')