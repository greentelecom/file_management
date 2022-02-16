import json
import traceback
import sys
import random
import requests
import os

sys.path.append("../models")
sys.path.append("../utilities_core")

from sqlalchemy import func, extract, desc, asc, Integer, String
from database_connect import SessionBase, Session, engine

from werkzeug.utils import secure_filename
from date_utilities import DateUtilities
from logger_factory import LoggerFactory
from tbl_bank_transactions import BankTxn
from tbl_partner_transaction import PartnerTxn
from .method_factory import MethodFactory
from users_table import Users

def generate_access_token():
    try:
        server_url = 'https://httpbin.org/put'
        payload = '{"message":"","mismatchAmount":"","transaction":[{"transactionRef":"","account":"","amount":""},{"transactionRef":"","account":"","amount":""}}}'
        headers = {"Content-Type": "application/json",
                   "Content-length": "value",
                   "Cache-Control": "no-cache",
                   "Pragma": "no-cache",
                   "X-Requested-With": "XMLHttpRequest"
                   }

        print('Final Payload %s ' % (server_url))
        print('Payload: ' + payload)
        r = requests.post(str(server_url), data=payload, headers=headers)
        print(r.status_code)
        print(r.url)
        print('Response: '+r.text)
        # LoggerFactory.logger_info('\n\nMESSAGE REQUEST %s ' % (r.url))
        # # token_array = [r.text]
        # token_dict = ast.literal_eval(r.text)
        # # print(token_dict["token"])
        # LoggerFactory.logger_info('\n\nACCESS TOKEN %s ' % (token_dict["token"]))
        # return token_dict["token"]
    except Exception as exc:
        print('Something went wrong.. {generate_access_token} %s' % (exc))
        # LoggerFactory.logger_exception('Something went wrong..{generate_access_token}')
        traceback.print_exc()


if __name__ == '__main__':
    while True:
        currentHour = DateUtilities.getCurrentHour()
        currentMin = DateUtilities().getCurrentMin()
        currentSec = DateUtilities().getCurrentSeconds()
        if currentHour == 7:
            if currentMin == 0 and 35 <= currentSec <= 36:
                performance_rpt()
        time.sleep(0.2)


