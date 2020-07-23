# from bs4 import BeautifulSoup
import re
import math
from os import remove

def readText():
    f = open ('reut2-001.sgm','r');
    mensaje="";
    for line in f.readlines():
        print(line);
    f.close();


def readStopWords(dictStopWords):
    f = open ('stopwords.txt','r');
    message = f.read();

    patternStopWords = re.compile(r"([a-z']+)");
    listStopWords = patternStopWords.findall(message);
    for i in listStopWords:
        dictStopWords[i]=i;
    return dictStopWords;

def removeComma(Number):
    new = re.sub('(?<=\d),(?=\d)', '', Number);
    return new;

def totalEntropy(dictClass, numDocs):
    # hacer la suma de los result de cada una de las clases
    # dictClass={key:[nc, result]}
    sumEntropy=0;
    for key in dictClass:
        p=(dict.get(key)[1])/numDocs;
        result = p*math.log2(p);
        dictClass[key][1]=result;
        sumEntropy+=result;

    finalEntropy=-1*sumEntropy;
    return finalEntropy;


def readFile():
    f = open('temp.txt', 'r')
    data= f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll('TITLE')
    for content in contents:
        print (content.text)





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

def getData():
    f = open('temp.txt','r');
    regex = r".*TOPICS=\"YES\".*NEWID=\"(\d+).*"
    line = f.readline()
    matches = re.match(regex, line, re.MULTILINE);
    if(matches):
        g = open('docs.txt','a');
        g.write(matches.group(1) + '\n');
        

        


def createTempFile(document, dictClass, dictWords):
    f = open ('temp.txt','w');
    f.write(document);
    f.close();
    getData();
    




def readText(dictClass, dictWords):
    f = open ('reut2-001.sgm','r');
    g = open('clases.txt','w');
    h = open('docs.txt','w');
    i = open('dicc.txt','w');
    document="";
    cont=1;
    regex = r".*</REUTERS>";
    for line in f.readlines():
        matches = re.match(regex, line, re.MULTILINE);
        if matches and cont<=3:
            createTempFile(document, dictClass, dictWords);
            cont+=1;
            document=""
            print("Aquí termina --------------")
        else:
            document+=line;
    f.close();
    return cont-1; 


def main():
    generalEntropy=0;
    dictStopWords = {};
    # el dictClass necesita el nombre como key, el número de veces que aparece esa clase, y result(el resultado de p*log(p,2)) como espacios en valor
    # luego hacer la división del número de veces que aparece entre el número total de documentos
    # número de veces que aparece entre el número total de documentos = nc/N = p
    # log en base 2 de número de veces que aparece entre el número total de documentos = log(p,2)
    # y luego hacer la multiplicación de p*log(p,2) = result
    dictClass = {};
    # el dictWords necesita el nombre como key, el ni, el número de veces que aparece por clase,
    # clase a la que pertece, el p de la clase a la que pertenece, y el resultado de la empropía por termino como espacios del valor.
    # 
    dictWords = {};
    # readStopWords(dictStopWords);
    # removeComma(number1);
    numDocs=readText(dictClass, dictWords);

    # readFile();



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

