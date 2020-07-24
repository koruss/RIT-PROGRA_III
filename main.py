from bs4 import BeautifulSoup
import re
import math
from os import remove


def readStopWords(dictStopWords):
    f = open ('stopwords.txt','r');
    message = f.read();
    patternStopWords = re.compile(r"([a-z']+)");
    listStopWords = patternStopWords.findall(message);
    for i in listStopWords:
        dictStopWords[i]=i;
    return dictStopWords;

def removeStopWords(words, dictStopWords):
    regex = r'(\d+?(?<=\d)\.(?=\d)\d+|\w+)';
    cleanWords=[];
    for i in words:
        matches = re.match(regex, i);
        if matches and i not in dictStopWords:
            cleanWords.append(matches.group(1));

    return(cleanWords);  

def totalEntropy(dictClass, numDocs):
    # hacer la suma de los result de cada una de las clases
    # dictClass={key:[nc, result, [NEWID]]}
    sumEntropy=0;
    for key in dictClass:
        p=(dictClass.get(key)[0])/numDocs;
        result = p*math.log2(p);
        dictClass[key][1]=result;
        sumEntropy+=result;

    finalEntropy=-1*sumEntropy;
    return finalEntropy;



def termEntropy(dictClass, dictWords, numDocs):
    # por cada uno de los elementos del dictWords
    # hacer las siguientes operaciones
    # 1- ni*log(ni,2)
    # 2- (N-ni)*log(N-ni, 2)
    # 3- número de veces que aparece * log(número de veces que aparece, 2)
    # 4- (nc de la clase a la que pertenece - número de veces que aparece) * log(nc de la clase a la que pertenece - número de veces que aparece, 2)
    # ahora para dar el resultado final se hace:
    # (1 + 2 - 3 - 4) / N
    # meter ese valor en el diccionario en el termino que corresponde
    # 
    # dictWords={key:[ni, nic, class, nc, result, IGTerm]}
    for key in dictWords:
        op1=(dictWords.get(key)[0])*math.log2(dictWords.get(key)[0]);
        op2=(numDocs-(dictWords.get(key)[0]))*math.log2(numDocs-(dictWords.get(key)[0]));
        op3=(dictWords.get(key)[1])*math.log2(dictWords.get(key)[1]);
        op4=((dictClass.get(dictWords.get(key)[2])[0])-(dictWords.get(key)[1]))*math.log2((dictClass.get(dictWords.get(key)[2])[0])-(dictWords.get(key)[1]));
        result=(op1+op2-op3-op4)/numDocs;
        dictWords[key][4]=result;



def IG(dictWords, generalEntropy):
    # para cada uno de lo terminos hacer:
    # totalEntropy - termEntropy
    # hacer un escalafón con los resultados mostrando el resultado de IG y el termino
    for key in dictWords:
        IGTerm = generalEntropy-(dictWords.get(key)[4]);
        dictWords[key][5]=IGTerm;


def readFile(toGet):
    f = open('temp.txt', 'r')
    data= f.read()
    soup = BeautifulSoup(data, "xml")
    contents = soup.findAll(toGet)
    for content in contents:
        return content.text


def getData(dictClass, dictWords):
    # dictClass={key:[nc, result, [NEWID]]}
    f = open('temp.txt','r');
    regex = r".*TOPICS=\"YES\".*NEWID=\"(\d+).*"
    topic=readFile('TOPICS');
    if dictClass.get(topic):
        dictClass[topic][0]+=1;
    else:
        dictClass[topic]=[1,0,[]];
    
    line = f.readline()
    matches = re.match(regex, line, re.MULTILINE);
    if(matches):
        dictClass[topic][2].append(matches.group(1));
        

def getWords(dictClass, dictWords, dictStopWords, cont):
    text=readFile('BODY');
    wordsComma = re.sub('(?<=\d),(?=\d)', '', text);
    wordsLower = wordsComma.lower();
    wordsSplit = wordsLower.split();
    words = removeStopWords(wordsSplit, dictStopWords);
    for i in words:
        if dictWords.get(i):
            dictWords[i]



def createTempFile(document, dictClass, dictWords, dictStopWords, cont):
    f = open ('temp.txt','w');
    f.write(document);
    f.close();
    # getData(dictClass, dictWords);
    getWords(dictClass, dictWords, dictStopWords, cont);
    




def readText(dictClass, dictWords, dictStopWords):
    f = open ('reut2-001.sgm','r');
    g = open('clases.txt','w');
    h = open('docs.txt','w');
    i = open('dicc.txt','w');
    document="";
    max=10000000;
    cont=1;
    regex = r".*</REUTERS>";
    for line in f.readlines():
        matches = re.match(regex, line, re.MULTILINE);
        if matches and cont<=1:
            createTempFile(document, dictClass, dictWords, dictStopWords, cont);
            cont+=1;
            document=""
            # print("Aquí termina --------------")
        else:
            document+=line;
    f.close();
    return cont-1; 


def main():
    dictStopWords = {};
    # dictClass={key:[nc, result, [NEWID]]}
    # el dictClass necesita el nombre como key, el número de veces que aparece esa clase, y result(el resultado de p*log(p,2)) como espacios en valor,
    # y una lista con los NEWID si corresponde
    # luego hacer la división del número de veces que aparece entre el número total de documentos
    # número de veces que aparece entre el número total de documentos = nc/N = p
    # log en base 2 de número de veces que aparece entre el número total de documentos = log(p,2)
    # y luego hacer la multiplicación de p*log(p,2) = result
    dictClass = {};
    # dictWords={key:[ni, nci, class, pClass, result}
    # el dictWords necesita el nombre como key, el ni, el número de veces que aparece por clase,
    # clase a la que pertece, el p de la clase a la que pertenece, y el resultado de la empropía por termino como espacios del valor.
    # 
    dictWords = {};
    # readStopWords(dictStopWords);
    # removeComma(number1);
    readStopWords(dictStopWords);
    numDocs=readText(dictClass, dictWords, dictStopWords);
    # for i in dictClass:
    #     print(i+':'+str(dictClass[i]))
 
    generalEntropy=totalEntropy(dictClass, numDocs);
    # print(generalEntropy);
    
    # print(dictStopWords);


    

    # print("Ingrese la ruta del archivo que contiene los artículos noticiosos");
    # path = input();
    # print("Ingrese la cantidad de mejores términos que serán escogidos (numMejores)");
    # numMejores = input();
    # print("Ingrese la cantidad mínima de documentos por clase (minNc)");
    # minNc = input();
	# print("Ingrese la cantidad mínima de documentos por término (minNi)");
    # minNi = input();
	# print("Ingrese un prefijo para usar en los nombres de los archivos generados");
    # pref = input();


main();

