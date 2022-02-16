import json
import configparser
import traceback
import sys
import random
import requests

sys.path.append("./models")
sys.path.append("./utilities_core")

from sqlalchemy import func, extract, desc, asc
from database_connect import SessionBase, Session, engine
from subscribers_table import Subscribers
from date_utilities import DateUtilities
from number_multiplexer_table import NumberMultiplexer
from logger_factory import LoggerFactory

SessionBase.metadata.create_all(engine)

session = Session()


class MethodFactory:

    def get_mno(self, subscriber_msisdn):
        try:
            number_multiplexer = session.query(NumberMultiplexer.mno).filter(
                NumberMultiplexer.msisdn_prefix.like('%' + str(subscriber_msisdn)[:5] + '%')).first()
            print('PREFIX %s' % subscriber_msisdn[:5])
            print('MNO %s' % (number_multiplexer))
            print('MSISDN %s' % (subscriber_msisdn))
            session.commit()
            return str(number_multiplexer.mno)
        except Exception as exc:
            session.rollback()
            print('Something went wrong {get_mno} %s' % (exc))
            LoggerFactory.logger_exception('Something went wrong..{get_mno}')
            traceback.print_exc()
        finally:
            if session:
                session.close()

    def reverse_passcode(self, passcode_value):
        try:
            passcode = passcode_value
            passcode_x = str(passcode)
            passcode_r = passcode_x[::-1]
            slice_one = passcode_r[:2]
            slice_two = passcode_r[2:4]
            slice_three = passcode_r[4:]
            return slice_three + slice_two + slice_one
        except Exception as exc:
            print('Something went wrong {reverse_passcode} %s' % (exc))
            LoggerFactory.logger_exception('Something went wrong..{reverse_passcode}')
            traceback.print_exc()

    def sendMessage(self, msisdn, message):
        try:

            server_url = 'http://idt_sms_api:8580/rest/sms/push/api'

            payload = {'msisdn': msisdn.strip(), 'message': message}
            header = {'Content-Type': 'application/json'}

            print('Final Payload %s ' % (server_url))
            r = requests.post(str(server_url), json=payload, headers=header)
            # print r.status_code
            print(r.url)
            LoggerFactory.logger_info('\n\nMESSAGE REQUEST %s ' % (r.url))
            print(r.text)
            LoggerFactory.logger_info('\n\nMESSAGE RESPONSE %s ' % (r.text))

            return r.text
        except Exception as exc:
            print('Something went wrong.. {sendMessage} %s' % (exc))
            LoggerFactory.logger_exception('Something went wrong..{sendMessage}')
            traceback.print_exc()