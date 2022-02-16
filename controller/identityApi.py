import json
import configparser
import traceback
import sys
import random
import requests
import passlib

from flask import Flask, jsonify, request

sys.path.append("./models")
sys.path.append("./utilities_core")

from sqlalchemy import func, extract, desc, asc
from database_connect import SessionBase, Session, engine
from subscribers_table import Subscribers
from date_utilities import DateUtilities
from .method_factory import MethodFactory
from categories_table import QuestionCategoriese
from logger_factory import LoggerFactory
from identity_api_user_table import User
from admin_table import Admin
from otp_table import OtpMessage

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

sys.path.append(
    './controller')

SessionBase.metadata.create_all(engine)

session = Session()

app = Flask(__name__)


@app.route('/rest/api/identity/record_user', methods=['POST'])
def record_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        jsonify({'message': "missing arguments"}), 400  # missing arguments
    if session.query(User).filter_by(username=username).first() is not None:
        jsonify({'message': "existing user"}), 400  # existing user
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201
    # , {'Location': url_for('get_survey_numbers', id=user.user_id, _external=True)}


@app.route('/rest/android/soka/trivia/get_otp_message', methods=['POST'])
def get_otp_message():
    try:
        request_data = request.get_json()
        msisdn = request_data['msisdn']
        # activation_code = MethodFactory().randomValue()
        otp_m = str(random.randint(1000, 9999))
        activation_code = '<#> Your otp code is : ' + otp_m + ' evi/lo/6ODE'

        otpmessage = session.query(OtpMessage).filter(OtpMessage.msisdn == msisdn).order_by(
            desc(OtpMessage.record_date)).first()

        if otpmessage is not None:
            now_date_time = DateUtilities().getTodayHourMinSec()
            seconds = DateUtilities().getSecondsDifference(str(otpmessage.last_update), now_date_time)

            print('Number of seconds Passed: ' + str(seconds) + " Date IS: " + str(
                otpmessage.last_update) + " Now is " + str(now_date_time))

            if int(seconds) < 50:

                print('<<<<<<Warning Multiple generation of OTP is NOT allowed...>>>>>')
            else:
                data = {'otp_message': otp_m, 'last_update': DateUtilities().getTodayHourMinSec()}
                session.query(OtpMessage).filter(OtpMessage.msisdn == msisdn).update(data)
                session.commit()

                message = '%s' % (activation_code)

                # MethodFactory().sendMessage(msisdn, message)
                # _dict = {"MSISDN": msisdn, "SMS": message}
                # SmsChannelApi().send_content(_dict)

                server_url = 'http://idt_sms_api:8580/rest/sms/push/api'

                payload = {'msisdn': msisdn.strip(), 'message': message}
                header = {'Content-Type': 'application/json'}
                #
                print('Final Payload %s ' % (server_url))
                r = requests.post(str(server_url), json=payload, headers=header)
                # # print r.status_code
                print(r.url)
                LoggerFactory.logger_info('\n\nMESSAGE REQUEST %s ' % (r.url))
                print(r.text)
                LoggerFactory.logger_info('\n\nMESSAGE RESPONSE %s ' % (r.text))

                # return r.text

                return jsonify({'response': [
                    {'status': 'SUCCESS', 'message': 'otp sent successfully',
                     'error_code': 'error000', 'msisdn': msisdn}]})

        else:
            otp_message = OtpMessage(otp_m, msisdn, DateUtilities().getTodayHourMinSec())
            session.add(otp_message)

            message = '%s' % (activation_code)

            MethodFactory().sendMessage(msisdn, message)

        # print 'Final Payload %s ' % (server_url)
        # r = requests.post(str(server_url), json=payload, headers=header)

        session.commit()

        return jsonify({'response': [
            {'status': 'SUCCESS', 'message': 'otp sent successfully',
             'error_code': 'error000', 'msisdn': msisdn}]})

    except Exception as exc:
        session.rollback()
        print('Something went wrong {get_otp_message} %s ' % (exc))
        LoggerFactory.logger_exception('Something went wrong..{get_otp_message}')
        traceback.print_exc()

    finally:
        if session:
            session.close()
            # session.remove()


@app.route('/rest/android/biometric/identity/check_existance', methods=['POST'])
def check_existance():
    try:
        session = Session()
        request_data = request.get_json()
        msisdn = request_data['msisdn']
        deviceId = request_data['deviceId']
        subscriber_ = session.query(Subscribers).filter(Subscribers.msisdn == msisdn,
                                                        Subscribers.device_id == deviceId).first()
        if subscriber_ is not None:
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'customer exists',
                 'error_code': 'error000'}]})
        else:
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'customer not available',
                 'error_code': 'error999'}]})

        session.commit()
    except Exception as exc:
        session.rollback()
        print('Something went wrong {check_existance} %s ' % (exc))
        LoggerFactory.logger_exception('Something went wrong..{check_existance}')
        traceback.print_exc()
    finally:
        if session:
            session.close()
            # session.remove()


@app.route('/rest/android/biometric/identity/record_identity_info', methods=['POST'])
def record_identity_info():
    try:
        session = Session()
        request_data = request.get_json()
        msisdn = request_data['msisdn']
        deviceId = request_data['deviceId']
        txn_id = request_data['txn_id']

        subscriber_ = session.query(Subscribers).filter(Subscribers.msisdn == msisdn,
                                                        Subscribers.device_id == deviceId).first()
        if subscriber_ is not None:
            data_ = {"device_id": deviceId,
                     "last_update": DateUtilities().getTodayDate()}
            session.query(Subscribers).filter(Subscribers.msisdn == msisdn).update(data_)
            session.commit()
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'user updated successfully',
                 'error_code': 'error009'}]})
        else:
            subscriber = Subscribers(device_id=deviceId, msisdn=msisdn, mno="AIRTEL", identity_login_txnid=txn_id)
            session.add(subscriber)
            session.commit()
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'user recorded successfully',
                 'error_code': 'error009'}]})
        session.commit()
    except Exception as exc:
        session.rollback()
        LoggerFactory.logger_exception('Something went wrong..{record_kids_info}')
        traceback.print_exc()
        resp = jsonify({'message': 'Identity info not recorded, Check your request correctly'})
        resp.status_code = 400
        return resp
    finally:
        if session:
            session.close()


@app.route('/rest/android/biometric/identity/record_identity_admin_info', methods=['POST'])
def record_identity_admin_info():
    try:
        session = Session()
        request_data = request.get_json()
        msisdn = request_data['msisdn']
        deviceId = request_data['deviceId']
        finger_template = request_data['finger_template']

        admin_ = session.query(Admin).filter(Admin.msisdn == msisdn,
                                             Admin.device_id == deviceId).first()
        if admin_ is not None:
            data_ = {"device_id": deviceId,
                     "last_update": DateUtilities().getTodayDate(),
                     "finger_template": bytes((finger_template), encoding='utf8')}
            session.query(Admin).filter(Admin.msisdn == msisdn).update(data_)
            session.commit()
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'user updated successfully',
                 'error_code': 'error009'}]})
        else:
            admn = Admin(device_id=deviceId, msisdn=msisdn, mno="AIRTEL",
                         finger_template=finger_template)
            session.add(admn)
            session.commit()
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'user recorded successfully',
                 'error_code': 'error009'}]})
        session.commit()
    except Exception as exc:
        session.rollback()
        LoggerFactory.logger_exception('Something went wrong..{record_identity_admin_info}')
        traceback.print_exc()
        resp = jsonify({'message': 'Identity info not recorded, Check your request correctly'})
        resp.status_code = 400
        return resp
    finally:
        if session:
            session.close()


@app.route('/rest/android/biometric/identity/get_identity_info', methods=['POST'])
def get_identity_info():
    try:
        # result_json_request = request.get_json()
        identity_object = session.query(Subscribers).all()
        response_array = []
        for identityObj in identity_object:
            response_body = (
                {"finger_template": identityObj.finger_template.decode("utf-8"), "msisdn": identityObj.msisdn})
            response_array += [response_body, ]

        print(response_array)
        session.commit()
        return jsonify({"response": response_array})

    except Exception as exc:
        session.rollback()
        print('Something went wrong {get_identity_info} %s ' % (exc))
        LoggerFactory.logger_exception('Something went wrong..{get_identity_info}')
        traceback.print_exc()
    finally:
        if session:
            session.close()
            # session.remove()


@app.route('/rest/android/biometric/identity/get_identity_passcode', methods=['POST'])
def get_identity_passcode():
    try:
        result_json_request = request.get_json()
        passcode = result_json_request['passcode']

        identity_object = session.query(Admin).filter(Admin.passcode == passcode).first()
        if identity_object is not None:
            session.commit()
            return jsonify({'response': [
                {'status': 'SUCCESS', 'message': 'passcode matched, user authenticated',
                 'error_code': 'error000'}]})
        else:
            new_passcode = MethodFactory().reverse_passcode(int(str(passcode)))
            identity_object_x = session.query(Admin).filter(Admin.passcode == new_passcode).first()
            if identity_object_x is not None:
                session.commit()
                return jsonify({'response': [
                    {'status': 'SUCCESS', 'message': 'passcode matched, user authenticated',
                     'error_code': 'error000'}]})
            else:
                return jsonify({'response': [
                    {'status': 'SUCCESS', 'message': 'passcode unmatched, user disqualified',
                     'error_code': 'error009'}]})

    except Exception as exc:
        session.rollback()
        print('Something went wrong {get_identity_passcode} %s ' % (exc))
        LoggerFactory.logger_exception('Something went wrong..{get_identity_passcode}')
        traceback.print_exc()
    finally:
        if session:
            session.close()
            # session.remove()


@app.route('/rest/android/biometric/identity/get_admin_identity_info', methods=['POST'])
def get_admin_identity_info():
    try:
        # result_json_request = request.get_json()
        identity_object = session.query(Admin).all()
        response_array = []
        for identityObj in identity_object:
            response_body = (
                {"finger_template": identityObj.finger_template.decode("utf-8"), "msisdn": identityObj.msisdn})
            response_array += [response_body, ]

        print(response_array)
        session.commit()
        return jsonify({"response": response_array})

    except Exception as exc:
        session.rollback()
        print('Something went wrong {get_admin_identity_info} %s ' % (exc))
        LoggerFactory.logger_exception('Something went wrong..{get_admin_identity_info}')
        traceback.print_exc()
    finally:
        if session:
            session.close()
            # session.remove()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8489)
