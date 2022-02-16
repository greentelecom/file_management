import sys
import time
import traceback
import xlsxwriter
import smtplib
import os.path

import xml.etree.ElementTree as ET
from sqlalchemy.sql.elements import or_
# import mysql.connector
# from mysql.connector import Error


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

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SessionBase.metadata.create_all(engine)
session = Session()


def send_email():
    try:
        email = 'jackson.nduke@mainstreammedia.co.tz'
        password = 'Nduke@123'
        send_to_email = ['inhousedevelopments@nbc.co.tz']

        # send_to_email = 'Deogratius.Lazari@connectmoja.co.tz'
        # send_to_email = 'ndukep@gmail.com'
        subject = 'Bank B and Company X Total Mismatch Amount For February 16 is xxx'
        message = ''
        file_location = 'C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\REPORTS\\x_transactions_report' + DateUtilities().getPreviousDate(
            1) + '.xlsx'

        # print 'Email is %s' % (configr.notification_email)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = ", ".join(send_to_email)
        msg['Subject'] = subject

        workbook = xlsxwriter.Workbook(
            'C:\\Users\\nduke\\Documents\\BANK_PROJECT\\UPLOADS\\REPORTS\\x_transactions_report_' + DateUtilities().getPreviousDate(
                1) + '.xlsx')

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '$#,##0'})

        cell_format = workbook.add_format({'bold': True, 'bg_color': '#DCDCDC'})

        # Create a workbook and add a worksheet.

        worksheet = workbook.add_worksheet()

        activities = ()

        total_match_amount = 0
        total_interactions = 0

        partner_x_compare = session.query(PartnerTxn).filter(PartnerTxn.institution == "X").all()
        data_x_match = []
        for x_details in partner_x_compare:
            x_report_list = []
            match_proof = session.query(BankTxn).filter(BankTxn.account == x_details.account,
                                                        BankTxn.amount == x_details.amount).first()
            if match_proof is not None:
                x_report_list.append(x_details.amount)
            else:
                x_report_list.append(x_details.amount)

            activities += (x_report_list,)
            session.commit()
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        worksheet.write(row, col, "Mismatch", bold)
        worksheet.write(row, col + 1, "Match", bold)

        row += 1

        for match, mismatch in (activities):
            worksheet.write(row, col, match)
            worksheet.write(row, col + 1, mismatch)
            row += 1

        # Write a total using a formula.
        worksheet.write(row, 0, 'Total', cell_format)
        worksheet.write(row, 1, '=SUM(A2:A25)', cell_format)
        worksheet.write(row, 2, '=SUM(B2:B25)', cell_format)

        # Create a new chart object.
        chart = workbook.add_chart({'type': 'line'})

        # Add a series to the chart.
        chart.add_series({'values': '=Sheet1!$A$2:$A$25', 'marker': {'type': 'diamond'}})

        # Insert the chart into the worksheet.
        worksheet.insert_chart('J2', chart)

        workbook.close()

        message = 'Hi, \n\n Attached is a performance report for JipimePlus  on ' + DateUtilities().getPreviousDate(
            1) + '  Your Yesterday Revenue was ' + str(total_revenue) + ',  and Total of ' + str(
            total_interactions) + ' Success Interactions were made. \n\n' \
                                  'Incase of further clarifications please contact ndukep@gmail.com'

        msg.attach(MIMEText(message, 'plain'))
        # Setup the attachment
        filename = os.path.basename(file_location)
        attachment = open(file_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Attach the attachment to the MIMEMultipart object
        msg.attach(part)
        server = smtplib.SMTP('mail.mainstreammedia.co.tz', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()
        time.sleep(0.2)

    except Exception as exc:
        print('Something went wrong.. {performance_report} %s' % (exc))
        LoggerFactory.logger_exception('Something went wrong.. {performance_report}')
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






