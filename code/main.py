import io

import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import spacy
from spacy.lang.en.tokenizer_exceptions import string

import re
import functions as f
import preprocess as pre
import nltk.data
from nltk import sent_tokenize
# nltk.download()

# enter pdf document
fname = input("Enter the path of the pdf:")

# covert pdf to text file
#p2t.pdf_to_text(doc_path)
# pt.convert(fname)

def convert(fname,pages=None):
    infile = open(fname, 'rb')
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

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
# print(x)

# read the text file
file = open("myfile.txt", "rt")
data = file.read()


# remove page numbers
page = re.sub(r'(\s([?,.!"]))|(?<=\[|\()(.*?)(?=\)|\])', lambda x: x.group().strip(), data)
pageNumRegex = re.compile(r'(\([0-9]+\))')
result = pageNumRegex.sub("", page)


# convert text to upper case
result = result.upper()
#print(result)

# remove short forms
def preprocess(text):
    # vs
    text = text.replace("V.", "VS")
    text = text.replace("VS.", "VS")
    text = text.replace("VS", "VS")
    # primary court
    text = text.replace("P. C.", "PRIMARY COURT")
    text = text.replace("P. C", "PRIMARY COURT")
    text = text.replace("P.C.", "PRIMARY COURT")
    text = text.replace("PC", "PRIMARY COURT")
    text = text.replace("PC.", "PRIMARY COURT")
    text = text.replace("P.C", "PRIMARY COURT")
    # district court
    text = text.replace("D. C.", "DISTRICT COURT")
    text = text.replace("D. C", "DISTRICT COURT")
    text = text.replace("D.C.", "DISTRICT COURT")
    text = text.replace("DC", "DISTRICT COURT")
    text = text.replace("DC.", "DISTRICT COURT")
    text = text.replace("D.C", "DISTRICT COURT")
    # magistrate court
    text = text.replace("M. C.", "MAGISTRATE COURT")
    text = text.replace("M. C", "MAGISTRATE COURT")
    text = text.replace("M.C.", "MAGISTRATE COURT")
    text = text.replace("MC", "MAGISTRATE COURT")
    text = text.replace("MC.", "MAGISTRATE COURT")
    text = text.replace("M.C", "MAGISTRATE COURT")
    # supreme court
    text = text.replace("S.C.", "SUPREME COURT")
    text = text.replace("S. C", "SUPREME COURT")
    text = text.replace("S.C.", "SUPREME COURT")
    text = text.replace("SC", "SUPREME COURT")
    text = text.replace("SC.", "SUPREME COURT")
    text = text.replace("S.C", "SUPREME COURT")
    # commercial high court
    text = text.replace("CHC", "COMMERCIAL HIGH COURT")
    # high court
    text = text.replace("H.C.", "HIGH COURT")
    text = text.replace("H. C", "HIGH COURT")
    text = text.replace("H.C.", "HIGH COURT")
    text = text.replace("HC", "HIGH COURT")
    text = text.replace("HC.", "HIGH COURT")
    text = text.replace("H.C", "HIGH COURT")
    # other forms
    text = text.replace("NO.", "NO")
    text = text.replace("RS.", "RS")
    text = text.replace("HTTPS://WWW", " ")
    text = text.replace("10/31/2020", " ")
    text = text.replace("-", " ")
    return text


result = preprocess(result)
#print(result)

# split into sentences
sentences_list = []
from nltk import sent_tokenize
sentences_list = sent_tokenize(result)
#print(sentences_list)

previous_judgment_list = []


# ................find case name.............#

name = ''
for sentence in sentences_list:
    if sentence.count('VS') > 0:
        print("Case Name:" + sentence)
        name = sentence
    break



# ............... find court ................#

court_search = ["PRIMARY COURT", "DISTRICT COURT", "MAGISTRATE COURT", "SUPREME COURT", "COURT OF APPEAL",
                "LABOUR COURTS", "JUDICIAL SERVICE COMMISSION", "C.R"]
count = 0;
for sentence in sentences_list:
    for i in range(8):
        if sentence.count(court_search[i]) > 0:
            count = count + 1
            if count == 1:
                print("Court and Reference Number:" + sentence)



# ...............find judgement date........#

# get dates of the txt file
pattern = re.findall(r"\d{1,2}\w{0,2}\s\w+\W\s\d\d\d\d",result)

res = [int(sub.split(', ')[1]) for sub in pattern]

# find the nearest date
if len(res) > 1:

    for i in range(len(res)-1):
        if res[i] > res[i+1]:
            x = res[i]

    matches = []
    for match in pattern:
        if str(x) in match:
                matches.append(match)

    print('Judgment date:',matches)  # print the Judgment date

else:
    print('Judgment date:', pattern)  # print the Judgment date



# ................judges names and decision...............#

def check(sentences_list, words):
    res = [all([k in s for k in words]) for s in sentences_list]
    return [sentences_list[i] for i in range(0, len(res)) if res[i]]


words = ['J.']
judges_names = check(sentences_list, words)
print('Judges names and decision: ', *judges_names, sep="\n")

'''
there is problem that if there is any word with "J." it also taken as a judge name
'''

# .................find previous cases.......#

previous_judgments = ["THE CASE OF", "THE JUDGMENT OF", "VIDE", "VS", "HELD IN"]
count = 0
for sentence in sentences_list:
    tokens = nltk.word_tokenize(sentence)
    for i in range(4):
        for token in tokens:
            if token == previous_judgments[i]:
                if (i == 3):
                    count = count + 1
                    if (count > 1):
                        previous_judgment_list.append(sentence)

                else:
                    previous_judgment_list.append(sentence)

if len(previous_judgment_list) > 0:
    print("The Previous Judgements:")
else:
    print("No previous judgments")

for p in previous_judgment_list:
    if (p != name):
        print(p)

# print(name)

# .............legal concepts....................#

pattern1 = "\bSECTION\s\d+\s\w+\s\w+\s\w+\s\w+\s+\w+\b"
pattern2 = "\bSECTION\s\d+\s\w+\s\w+\s\w+\s\w{4}\b"
pattern3 = "\bCOPYRIGHT\s\w+\s\w+\s\w+\s\w+\b"
pattern4 = "\bSECTION\s\d+\s\w{2}\s\w{3}\s\w+\s\w{2}\s+\w+\s\w+\s\w{3}\s\w+\s\d+\s\w{2}\s\d+\b"

match1 = re.findall(r"\bSECTION\s\d+\s\w{2}\s\w{3}\s\w+\s\w+\s+\w+\b", result)
match2 = re.findall(r"\bSECTION\s\d+\s\w{2}\s\w+\s\w+\s\w{4}\b",result)
match3 = re.findall(r"\bCOPYRIGHT\s\w+\s\w+\s\w+\s\w+\b",result)
match4 = re.findall(r"\bSECTION\s\d+\s\w{2}\s\w{3}\s\w+\s\w{2}\s+\w+\s\w+\s\w{3}\s\w+\s\d+\s\w{2}\s\d+\b",result)

matches = []
matches = match1 + match2 + match3 + match4

concepts = []
for i in matches:
    if i not in concepts:
        concepts.append(i)

print('Legal concepts used: ',concepts)


# .............Keywords....................#

vocab_dict , arr = pre.textProcessing(data)
tf = f.computeTF(vocab_dict,arr)
idf = f.computeIDF([vocab_dict])
keywords = f.computeTfidf(tf,idf)

with open("keywords.txt", "w") as outfile:
    outfile.write("\n".join(keywords))

print('keywords:')
print(keywords)







