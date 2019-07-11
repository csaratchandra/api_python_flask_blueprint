from app.api import bp
import pandas as pd
import glob
import os
from flask import jsonify
from app.api.errors import error_response
import json


@bp.route('/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """    
     Returns information about a single transaction id

     Parameters
     ----------
     transaction_id : integer, required
         Transaction id about which information is requested.
    """   
    # Multiple File Handling
    appended_data = []
    api_dir = os.path.dirname(__file__)
    
    trans_file_path = os.path.join(api_dir, 'data/transaction/')
    ref_file_path   = os.path.join(api_dir, 'data/reference/')

    all_trans_files = glob.glob(trans_file_path + '*.csv')
    

    for a_file in all_trans_files:
        read_data = pd.read_csv(a_file, index_col=None, header=0)
        appended_data.append(read_data)
    
    ref_data = pd.read_csv(ref_file_path + 'ProductReference.csv')
        
    df = pd.concat(appended_data, axis=0, ignore_index=True)
    df = df[df.transactionId == transaction_id]

    
    if df.empty:
        return error_response(404)
    else:

        # There is no mention of unique transaction id in the assignment,
        # but assuming ids will be unique and dropping duplicates on them 
        # duplicates are here due to test data.

        df = df.drop_duplicates(subset='transactionId', keep='last',inplace=False)
        
        df = pd.merge(df,ref_data,on='productId',how='left',indicator=True)
        df = df[['transactionId', 'productName', 'transactionAmount', 'transactionDatetime']]
        payload = df.to_dict('records')        

        print(payload[0])

        return jsonify(payload[0])
 # """   
    
@bp.route('/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
def get_product_summary(last_n_days):
    """
    Returns product summary from last_n_days

    Parameters
    ----------
    last_n_days : integer, required
        Denotes days, used to provide transaction summary at product level for provided days.
    """    
    # Multiple File Handling
    appended_data = []
    api_dir = os.path.dirname(__file__)
    
    trans_file_path = os.path.join(api_dir, 'data/transaction/')
    ref_file_path   = os.path.join(api_dir, 'data/reference/')

    all_trans_files = glob.glob(trans_file_path + '*.csv')
    

    for a_file in all_trans_files:
        read_data = pd.read_csv(a_file, index_col=None, header=0)
        appended_data.append(read_data)
    
    ref_data = pd.read_csv(ref_file_path + 'ProductReference.csv')
        
    df = pd.concat(appended_data, axis=0, ignore_index=True)
    
    df['transactionDatetime'] = df['transactionDatetime'].astype('datetime64[ns]')
    cutoff_date = df['transactionDatetime'].iloc[-1] - pd.Timedelta(days=last_n_days)
    df = df[df.transactionDatetime > cutoff_date] 
    df = pd.DataFrame(df.groupby('productId').transactionAmount.sum())
    df = df.reset_index()
    df = df.rename(columns={'transactionAmount':'totalAmount'})
    df = pd.merge(df,ref_data,on='productId',how='left',indicator=True)
    df = df[['productName', 'totalAmount']]

    print(df)
    return jsonify(summary=df.to_dict('records'))

@bp.route('/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
def get_transaction_summary(last_n_days):
    """
    Returns transaction summary from last_n_days

    Parameters
    ----------
    last_n_days : integer, required
        Denotes days, used to provide transaction summary at city level for provided days.
    """
        # Multiple File Handling
    appended_data = []
    api_dir = os.path.dirname(__file__)
    
    trans_file_path = os.path.join(api_dir, 'data/transaction/')
    ref_file_path   = os.path.join(api_dir, 'data/reference/')

    all_trans_files = glob.glob(trans_file_path + '*.csv')
    

    for a_file in all_trans_files:
        read_data = pd.read_csv(a_file, index_col=None, header=0)
        appended_data.append(read_data)
    
    ref_data = pd.read_csv(ref_file_path + 'ProductReference.csv')
        
    df = pd.concat(appended_data, axis=0, ignore_index=True)

    df['transactionDatetime'] = df['transactionDatetime'].astype('datetime64[ns]')
    cutoff_date = df['transactionDatetime'].iloc[-1] - pd.Timedelta(days=last_n_days)
    df = df[df.transactionDatetime > cutoff_date] 

    df = pd.merge(df,ref_data,on='productId',how='left',indicator=True)
    df = pd.DataFrame(df.groupby('productManufacturingCity').transactionAmount.sum())
    df = df.reset_index()
    df = df.rename(columns={"productManufacturingCity":"cityName","transactionAmount":"totalAmount"})
    print(df)
    
    return jsonify(summary=df.to_dict('records'))