#EXTRACT TEXT FROM PDF AND SAVE TO A TEXT FILE
import slate3k as slate
import PyPDF2

def pdf_to_text(docPath):
    pdfFileObject = open(docPath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages

    with open(docPath, 'rb') as f:
        extracted_text=slate.PDF(f)

    file1 = open("myfile.txt","w")

    for i in range(0,count):
        file1.writelines(extracted_text[i]) #write extracted text into a text file
    file1.close()
