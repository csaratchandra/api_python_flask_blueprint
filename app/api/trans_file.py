import os
import glob
import pandas as pd

def process_file(transfile,productfile):
    """
    Reads the transactiona and references files and prepares them for further processing.
    """
    appended_data = []
    api_dir = os.path.dirname(__file__)
    
    trans_file_path = os.path.join(api_dir, 'data/transaction/')
    ref_file_path   = os.path.join(api_dir, 'data/reference/')

    all_trans_files = glob.glob(trans_file_path + transfile)
    
    for a_file in all_trans_files:
        read_data = pd.read_csv(a_file, index_col=None, header=0,skipinitialspace=True)
        appended_data.append(read_data)
    
    ref_data = pd.read_csv(ref_file_path + productfile)
        
    trans_data = pd.concat(appended_data, axis=0, ignore_index=True)

    return trans_data,ref_data