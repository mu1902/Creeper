import datetime
import os

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from win32com.client import Dispatch

import Creeper as cp

if __name__ == '__main__':
    # dn = datetime.date(2018,1,1)
    # print(cp.tool.isHoliday(dn))

    cp.tool.send_email([], 'test', '测试')

    # current_file_path = os.path.dirname(os.path.abspath(__name__))
    # print(current_file_path)

    # project_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
    # print(project_file_path)

    # print(__file__)
    # print(__name__)
    # print(__doc__)
