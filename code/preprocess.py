import spacy

nlp = spacy.load("en_core_web_sm")
file = open("myfile.txt", "rt")
data = file.read()

def textProcessing(doc):
    '''Prepocessing of input text with 
    1. tokenisation and Lemmatisation
    2. Removing stop words 
    3. Creating and removing custom stop words.
    4. Generating required Vocabulary from input
    5. Preprocessing the input 
    '''
    Nouns = []
    Noun_set = []
    trimmed_noun_set = []
    removing_duplicates = []
    arr = []
    vocab = []
    vocab_dict = {}

    doc = nlp(doc.upper())#Convert to upper case

    for possible_nouns in doc:
        if possible_nouns.pos_ in ["NOUN","PROPN"] : #PROPN ->Proper Nouns 
            Nouns.append([possible_nouns , [child for child in possible_nouns.children]]) #append all nouns and pronouns into nouns[] array
       
    
    for i,j in Nouns:
        for k in j:
            Noun_set.append([k,i])

    
    for i , j in Noun_set:
        if i.pos_ in ['PROPN','NOUN','ADJ']:
            trimmed_noun_set.append([i ,j])
            
    
    for word in trimmed_noun_set:
        if word not in removing_duplicates:
            removing_duplicates.append(word)
    
    
    for i in removing_duplicates:
        strs = ''
        for j in i:
            strs += str(j)+" "
        arr.append(strs.strip())

    
    for word in Noun_set:
        string = ''
        for j in word:
            string+= str(j)+ " "
        vocab.append(string.strip())

    
    for word in vocab:
        vocab_dict[word]= 0
        
    for word in arr:
        vocab_dict[word]+= 1

    return vocab_dict,arr


