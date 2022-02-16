import json
import traceback
import sys
import random
import requests
import pandas as pd
import os
import csv
import xml.etree.ElementTree as ET
from sqlalchemy.sql.elements import or_
# import mysql.connector
# from mysql.connector import Error
from flask import Flask, jsonify, request, send_file, send_from_directory

sys.path.append("../models")
sys.path.append("../utilities_core")

from sqlalchemy import func, extract, desc, asc, Integer, String
from database_connect import SessionBase, Session, engine

from werkzeug.utils import secure_filename
from date_utilities import DateUtilities
from logger_factory import LoggerFactory
from tbl_bank_transactions import BankTxn
from tbl_partner_transaction import PartnerTxn
# from .method_factory import MethodFactory
# from users_table import Users

sys.path.append(
    '../controller')

SessionBase.metadata.create_all(engine)
session = Session()

UPLOAD_FOLDER = 'C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# The absolute path of the directory containing images for users to download
app.config["CLIENT_XLS"] = "/usr/local/tigo_kandanda/xls/"

app.config["CLIENT_XLSX"] = "C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\XLSX\\"

# The absolute path of the directory containing CSV files for users to download
app.config["CLIENT_CSV"] = "C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\CVS\\"

# The absolute path of the directory containing PDF files for users to download
app.config["CLIENT_TXT"] = "/usr/local/tigo_kandanda/txt/"

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xls', 'xlsx', 'ods'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/bank-b-engine/api/v1/transactions', methods=['POST'])
def upload_subscribers():
    try:
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_file = (app.config['UPLOAD_FOLDER'] + filename)
            print('Saved File Path: ' + str(saved_file))
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension == 'csv':
                subsribers_df = pd.read_csv(saved_file, encoding="ISO-8859-1", sep='[:,|,\t]', engine='python')

                index = 0
                for index, row in subsribers_df.iterrows():
                    txnRef_value = str(row['transactionRef']).upper()
                    account_value = str(row['account'])
                    amount_value = str(row['amount'])
                    subsribers_df.loc[index, 'amount'] = amount_value
                    subsribers_df.loc[index, 'account'] = account_value
                    subsribers_df.loc[index, 'transaction_ref'] = txnRef_value
                    subsribers_df.to_csv(saved_file, index=False)
                    index += 1

                    x_accounts = []
                    x_accounts.append(account_value)

                    table_name = 'partner_transactions'

                    subsribers_df.to_sql(
                        table_name,
                        engine,
                        if_exists='append',
                        index=False,
                        chunksize=500,
                        dtype={
                            "transaction_ref": String(60),
                            "amount": String(20),
                            "account": String(20)
                        }
                    )
                    data_ = {"institution": "X"}
                    session.query(PartnerTxn).filter(PartnerTxn.account.in_(y_accounts)).update(data_,
                                                                                                synchronize_session='fetch')

                    header = ['partner', 'amount', 'account', 'status']
                    data_partner = []

                    partner_x_compare = session.query(PartnerTxn).filter(PartnerTxn.institution == "X").all()
                    data_x_match = []
                    data_x_not_in_b = []
                    sum_of_x_not_in_b = 0
                    for x_details in partner_x_compare:
                        data_x_match.append(x_details.institution)
                        data_x_match.append(x_details.amount)
                        data_x_match.append(x_details.account)
                        match_proof = session.query(BankTxn).filter(BankTxn.account == x_details.account,
                                                                    BankTxn.amount == x_details.amount).first()
                        if match_proof is not None:
                            data_x_match.append("true")
                        else:
                            data_x_match.append("false")
                            sum_of_x_not_in_b += float(x_details.amount)

                    data_x_not_in_b.append("X")
                    data_x_not_in_b.append(sum_of_x_not_in_b)

                    data_partner.append(data_x_match)

                    with open('C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\REPORTS\\partner_x_match.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        # write the header
                        writer.writerow(header)

                        # write multiple rows
                        writer.writerows(data_partner)

                    header_x = ['partner', 'amount_not_in_b']


                    with open('C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\REPORTS\\x_not_in_b.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        # write the header
                        writer.writerow(header_x)

                        # write the data
                        writer.writerow(data_x_not_in_b)


            elif file_extension == 'xls' or file_extension == 'xlsx':
                subsribers_df = pd.read_excel(saved_file, encoding="ISO-8859-1", sep='[:,|,\t]', engine='python')

                index = 0
                for index, row in subsribers_df.iterrows():
                    txnRef_value = str(row['transactionRef']).upper()
                    account_value = str(row['account'])
                    amount_value = str(row['amount'])
                    subsribers_df.loc[index, 'amount'] = amount_value
                    subsribers_df.loc[index, 'account'] = account_value
                    subsribers_df.loc[index, 'transaction_ref'] = txnRef_value
                    subsribers_df.to_excel(saved_file, index=False)
                    index += 1

                    y_accounts = []
                    y_accounts.append(account_value)

                    table_name = 'partner_transactions'

                    subsribers_df.to_sql(
                        table_name,
                        engine,
                        if_exists='append',
                        index=False,
                        chunksize=500,
                        dtype={
                            "transaction_ref": String(60),
                            "amount": String(20),
                            "account": String(20)
                        }
                    )
                    data_ = {"institution": "Y"}
                    session.query(PartnerTxn).filter(PartnerTxn.account.in_(y_accounts)).update(data_,
                                                                                                synchronize_session='fetch')

                    header = ['partner', 'amount', 'account', 'status']
                    data_partner = []

                    partner_y_compare = session.query(PartnerTxn).filter(PartnerTxn.institution == "Y").all()
                    data_y_match = []
                    for y_details in partner_y_compare:
                        data_y_match.append(y_details.institution)
                        data_y_match.append(y_details.amount)
                        data_y_match.append(y_details.account)
                        match_proof = session.query(BankTxn).filter(BankTxn.account == y_details.account,BankTxn.amount == y_details.amount).first()
                        if match_proof is not None:
                            data_y_match.append("true")
                        else:
                            data_y_match.append("false")
                    data_partner.append(data_y_match)

                    with open('C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\REPORTS\\partner_y_match.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        # write the header
                        writer.writerow(header)

                        # write multiple rows
                        writer.writerows(data_partner)

            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Allowed file types are txt, csv, xls,xlsx,ods'})
            resp.status_code = 400
            return resp
    except Exception as e:
        session.rollback()
        traceback.print_exc()
        resp = jsonify({'message': 'Uploading failed, violates unique constraint'})
        resp.status_code = 400
        return resp

        # traceback.print_exc()
    finally:
        if session:
            session.close()
