from app.api import bp
import pandas as pd
from flask import jsonify
from app.api.errors import error_response

# trans file and transaction file locations are stored in trans_file
from .trans_file import process_file


@bp.route('/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """    
     Returns information about a single transaction id

     Parameters
     ----------
     transaction_id : integer, required
         Transaction id about which information is requested.
    """   
    
    # File processing
    product_reference_file = 'ProductReference.csv'
    all_trans_files        = '*.csv'
    trans_data,ref_data = process_file(all_trans_files,product_reference_file)
    
    if trans_data.empty:
        return error_response(404)
    else:

        # Filtering on transaction id sent in request.
        trans_data = trans_data[trans_data.transactionId == transaction_id]

        # There is no mention of unique transaction id in the assignment,
        # but assuming ids will be unique and dropping duplicates on them 
        # duplicates are here due to test data.
        trans_data = trans_data.drop_duplicates(subset='transactionId', keep='last',inplace=False)
        
        # Preparing response to send back
        trans_data = pd.merge(trans_data,ref_data,on='productId',how='left',indicator=True)
        trans_data = trans_data[['transactionId', 'productName', 'transactionAmount', 'transactionDatetime']]
        payload = trans_data.to_dict('records')        

        return jsonify(payload[0])

    
@bp.route('/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
def get_product_summary(last_n_days):
    """
    Returns product summary from last_n_days

    Parameters
    ----------
    last_n_days : integer, required
        Denotes days, used to provide transaction summary at product level for provided days.
    """
    # File processing    
    product_reference_file = 'ProductReference.csv'
    all_trans_files        = '*.csv'
    trans_data,ref_data = process_file(all_trans_files,product_reference_file)

    if trans_data.empty:
        return error_response(404)
    else:
        # Determining cutoff_data based on the # of days sent in request.
        trans_data['transactionDatetime'] = trans_data['transactionDatetime'].astype('datetime64[ns]')
        cutoff_date = trans_data['transactionDatetime'].iloc[-1] - pd.Timedelta(days=last_n_days)

        # Processing to determine transaction amount summary at product level
        trans_data = trans_data[trans_data.transactionDatetime > cutoff_date] 
        trans_data = pd.DataFrame(trans_data.groupby('productId').transactionAmount.sum())
        trans_data = trans_data.reset_index()
        trans_data = trans_data.rename(columns={'transactionAmount':'totalAmount'})
        trans_data = pd.merge(trans_data,ref_data,on='productId',how='left',indicator=True)
        trans_data = trans_data[['productName', 'totalAmount']]
        
        return jsonify(summary=trans_data.to_dict('records'))

@bp.route('/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
def get_transaction_summary(last_n_days):
    """
    Returns transaction summary from last_n_days

    Parameters
    ----------
    last_n_days : integer, required
        Denotes days, used to provide transaction summary at city level for provided days.
    """
    # File processing
    product_reference_file = 'ProductReference.csv'
    all_trans_files        = '*.csv'
    trans_data,ref_data = process_file(all_trans_files,product_reference_file)

    if trans_data.empty:
        return error_response(404)
    else:
        # Determining cutoff_data based on the # of days sent in request.
        trans_data['transactionDatetime'] = trans_data['transactionDatetime'].astype('datetime64[ns]')
        cutoff_date = trans_data['transactionDatetime'].iloc[-1] - pd.Timedelta(days=last_n_days)
        
        # Processing to determine transaction amount summary at city level
        trans_data = trans_data[trans_data.transactionDatetime > cutoff_date] 
        trans_data = pd.merge(trans_data,ref_data,on='productId',how='left',indicator=True)
        trans_data = pd.DataFrame(trans_data.groupby('productManufacturingCity').transactionAmount.sum())
        trans_data = trans_data.reset_index()
        trans_data = trans_data.rename(columns={"productManufacturingCity":"cityName","transactionAmount":"totalAmount"})
        
        return jsonify(summary=trans_data.to_dict('records'))