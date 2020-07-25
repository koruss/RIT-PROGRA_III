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
    #
    # dictWords[key]=[ni, cont, {classWord:1}, result, IG];
    # for i in dictWords['a'][1]:
    #     print(dictWords['a'][1][i]);
    print(dictClass.get('coffee'))
    print(dictWords.get('said'))
    for key in dictWords:
        ni=dictWords[key][0]
        Nmni = (numDocs - ni)

        op1=(ni)*(math.log2(ni));
        op2=(Nmni)*(math.log2(Nmni));
        op3=0;
        op4=0;
        for i in dictWords.get(key)[2]:
            nik=(dictWords.get(key)[2][i])
            op3+=(nik*(math.log2(nik)))

        for i in dictWords.get(key)[2]:
            nik=(dictWords.get(key)[2][i])
            nc=(dictClass.get(i)[0])
            ncmnik=(nc-nik)
            if ncmnik>0:
                print(key+': nc='+str(nc)+', nik='+str(nik)+', ncmnik='+str(ncmnik))
                op4+=((ncmnik)*(math.log2(ncmnik)))

        num=(op1+op2-op3-op4)
        result=num/numDocs;
        dictWords[key][3]=result;



def IG(dictWords, generalEntropy):
    # para cada uno de lo terminos hacer:
    # totalEntropy - termEntropy
    # hacer un escalafón con los resultados mostrando el resultado de IG y el termino
    for key in dictWords:
        IGTerm = generalEntropy-(dictWords.get(key)[3]);
        dictWords[key][4]=IGTerm;


def readTopic(toGet):
    f = open('temp.txt', 'r')
    data= f.read()
    soup = BeautifulSoup(data, "xml")
    contents = soup.findAll(toGet)
    for content in contents:
        if content.text!='':
            for i in content:
                return i.text;
                break;
        else:
            return content.text;
        
def readBody(toGet):
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
    topic=readTopic('TOPICS');
    if dictClass.get(topic):
        dictClass[topic][0]+=1;
    else:
        dictClass[topic]=[1,0,[]];
    
    line = f.readline()
    matches = re.match(regex, line, re.MULTILINE);
    if(matches):
        dictClass[topic][2].append(matches.group(1));
        

def getWords(dictClass, dictWords, dictStopWords, cont):

    # dictWords = {key: ni, cont, [class, class]}
    text='';
    text=readBody('BODY');
    classWord=readTopic('TOPICS');
    if text != None:
        wordsComma = re.sub('(?<=\d),(?=\d)', '', text);
        wordsLower = wordsComma.lower();
        wordsSplit = wordsLower.split();
        words = removeStopWords(wordsSplit, dictStopWords);
        for i in words:
            if (dictWords.get(i) and cont != dictWords[i][1]):
                dictWords[i][0]+=1;
                dictWords[i][1] = cont; 
                if (dictWords[i][2].get(classWord)):
                    dictWords[i][2][classWord] += 1;
                else:
                    dictWords[i][2][classWord] = 1;
            elif (dictWords.get(i)==None):
                dictWords[i]=[1, cont, {classWord:1}, 0, 0];
                

    # print(dictWords);



def createTempFile(document, dictClass, dictWords, dictStopWords, cont):
    f = open ('temp.txt','w');
    f.write(document);
    f.close();
    getData(dictClass, dictWords);
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
        if matches and cont<=max:
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
    readStopWords(dictStopWords);
    numDocs=readText(dictClass, dictWords, dictStopWords);
 
    generalEntropy=totalEntropy(dictClass, numDocs);
    termEntropy(dictClass, dictWords, numDocs);

    IG(dictWords, generalEntropy);

    

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

