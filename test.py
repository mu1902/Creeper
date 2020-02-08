import datetime
import os.path

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from win32com.client import Dispatch

import Creeper as cp

if __name__ == '__main__':
    # dn = datetime.date(2018,1,1)
    # print(cp.tool.isHoliday(dn))

    # cp.tool.send_email([], 'test', '无', 'html', 'utf')

    url = 'http://static.cninfo.com.cn/finalpage/2020-02-07/1207298265.docx'
    file_name = os.path.split(url)[-1]
    file_ext = file_name.split('.')[-1]
    file_url = os.getcwd() + '\\tmp\\' + file_name
    f = cp.downloader.get_file(url, file_url)
    if file_ext == 'doc' or file_ext == 'docx':
        word = Dispatch('Word.Application')
        doc = word.Documents.Open(file_url)
        file_name += ".pdf"
        file_ext = 'pdf'
        file_url += ".pdf"
        doc.SaveAs(file_url, FileFormat=17)
        doc.Close()
        word.Quit()

    if file_ext == 'pdf':
        try:
            f_pdf = pdfplumber.open(file_url)
            page = len(f_pdf.pages)
        except PDFSyntaxError:
            page = 0
        print(page)
