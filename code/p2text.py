import io

import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt

#fname = input("Enter the path of the pdf:")

#converts pdf, returns its text content as a string

def convert(fname):
    infile = open(fname, 'rb')
    pdfReader = PyPDF2.PdfFileReader(infile)
    pages = pdfReader.numPages
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    #infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    file1 = open("myfile.txt", "w")
    n = file1.write(text)
    file1.close()
    output.close
    return n

x=convert(fname)
print(x)


#converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
# def convertMultiple(pdfDir, txtDir):
#     if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in
#     for pdf in os.listdir(pdfDir): #iterate through pdfs in pdf directory
#         fileExtension = pdf.split(".")[-1]
#         if fileExtension == "pdf":
#             pdfFilename = pdfDir + pdf
#             text = convert(pdfFilename) #get string of text content of pdf
#             textFilename = txtDir +pdf+ ".txt"
#             textFile = open(textFilename, "w") #make text file
#             textFile.write(text) #write text to text file

# set paths accordingly:
pdfDir = "C:/Users/user/PycharmProjects/test/"
txtDir = "C://Users/user/PycharmProjects/test/"
# convertMultiple(pdfDir, txtDir)