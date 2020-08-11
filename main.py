from bs4 import BeautifulSoup
import re
import math
from os import remove
import operator
from operator import *
from tkinter.filedialog import *

def writeClass(dictClass, minNc,pref):
    g = open(pref+'clases.txt','w');
    h = open(pref+'docs.txt','w');
    word=""
    
    for i in dictClass:
        if dictClass.get(i)[0] >= minNc and dictClass.get(i)[2] != []:
            for l in dictClass.get(i)[2]:
                word=word+str(l)+" "
            h.write(i + ' ' + word + '\n')
            word=""
        if dictClass.get(i)[0] >= minNc:
            g.write(i + ' ' + str(dictClass.get(i)[0]) + '\n');
    g.close();

def writeDicc(dictWords, minNi,pref):    
    f = open(pref+'dicc.txt','w');
    for i in dictWords:
        if(dictWords[i][0] > minNi):
            f.write(i + ' ' + str(dictWords[i][0]) + '\n');
    f.close();


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



def termEntropy(dictClass, dictWords, numDocs, minNi):
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
    for key in dictWords:
        ni=dictWords[key][0]
        if ni > minNi:
            Nmni = (numDocs - ni)

            op1=(ni)*(math.log2(ni));
            if Nmni<=0:
                op2=0
            else:
                op2=(Nmni)*(math.log2(Nmni));

            op3=0;
            op4=0;
            for i in dictWords.get(key)[2]:
                nik=(dictWords.get(key)[2][i])
                op3+=(-(nik*(math.log2(nik))))

            ncmnik=0;
            num=0;
            arreglo= dictClass.keys()
            for clase in arreglo:
                num=dictWords.get(key)[2].get(clase)
                if(num!= None):
                    ncmnik=dictClass.get(clase)[0] - num
                else:
                    num=0;
                    ncmnik=ncmnik=dictClass.get(clase)[0]            
                if ncmnik<=0:
                    op4+=0;
                else:
                    op4+=(-((ncmnik)*(math.log2(ncmnik))));

            num=(op1+op2+op3+op4)
            
            result=(num/numDocs);
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
        # print (content)
        if content.text!='':
            for i in content:
                #print(i.text)
                return(i.text)
                break
        
def readBody(toGet):
    f = open('temp.txt', 'r')
    data= f.read()
    soup = BeautifulSoup(data, "xml")
    contents = soup.findAll(toGet)
    for content in contents:
        return content.text



def getClass(dictClass, numDocs):
    # numDocs={"num":0}
    # dictClass={key:[nc, result, [NEWID]]}
    f = open('temp.txt','r');
    regex = r".*TOPICS=\"YES\".*NEWID=\"(\d+).*"
    lines = f.readlines()
    topic=readTopic('TOPICS');
    # print(topic)
    for line in lines:
        matches = re.match(regex, line, re.MULTILINE);
        if(matches and topic != None):
            # valor+=1;
            numDocs["num"]=numDocs["num"]+1
            if dictClass.get(topic):
                dictClass[topic][0]+=1;
                dictClass[topic][2].append(matches.group(1));
            else:
                dictClass[topic]=[1,0,[matches.group(1)]];
    
    
    
        
        

def getWords(dictClass, dictWords, dictStopWords, cont, minNc):
    # dictClass={key:[nc, result, [NEWID]]}
    # dictWords = {key: ni, cont, [class, class], result, IG}
    text='';
    text=readBody('BODY');
    classWord=readTopic('TOPICS');
    if classWord in dictClass and dictClass.get(classWord)[0] > minNc and dictClass.get(classWord)[2] != []:
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
                


def createTempFile(document, dictClass, dictWords, dictStopWords, cont, first, minNc, numDocs):
    f = open ('temp.txt','w');
    f.write(document);
    f.close();
    if first == 0:
        getClass(dictClass, numDocs)
    else:
        getWords(dictClass, dictWords, dictStopWords, cont, minNc);
    
    




def readText(dictClass, dictWords, dictStopWords, first, minNc,path, numDocs):
    f = open(path, 'r')
    document="";
    max=10000000;
    cont=1;
    regex = r".*</REUTERS>";
    for line in f.readlines():
        matches = re.match(regex, line, re.MULTILINE);
        if matches and cont<=max:
            document=document+"</REUTERS>"
            createTempFile(document, dictClass, dictWords, dictStopWords, cont, first, minNc,numDocs);
            cont+=1;
            document=""
        else:
            document+=line;
    f.close();
    return cont-1; 

def get_GI(dict):
    # dictWords = {key: [ni, cont, [class, class], result, IG]}
    return dict.get('key')

def mejoresTerminos(num,dic):
    temp=[]  
    sortedList=sorted(dic.items())
    for word in sortedList:
        temp.append({'key':word[1][4], 'value':{'term':word[0], 'entropy':round(word[1][3],4),'GI':round(word[1][4],4)}})
    temp.sort(key=get_GI, reverse=True)
    escalafon=[]
    cont=0
    for element in temp:
         if(cont<num):
             value= element.get('value')
             escalafon.append([value.get('term'),value.get('entropy'),value.get('GI')])
             cont=cont+1
    return escalafon


def cleanWords(dictWords, minNi):
    temp={}
    for i in dictWords:
        if dictWords[i][0]>minNi:
            temp[i]=dictWords[i];

    return temp;

def writeGI(generalEntropy,dic,pref):
    f= open(pref+'GI.txt','w')
    for element in dic:
        f.write(str(generalEntropy)+" <"+ element+" "+str(round(dic[element][3],4))+" "+str( round(dic[element][4],4))+">\n" )
    f.close()

def writeBest(best,pref):
    f = open (pref+'mejores.txt','w');
    for i in best:
        f.write(str(i[0])+" "+str(i[1])+" "+str(i[2])+'\n');
    f.close();

def main():
    filepath = askopenfilename(title="Que archivo deseas analizar", filetypes=(("sgm", "*.sgm"),("All files", "*.*")))  # abre la ventanita de buscar archivos
    print("Ingrese la cantidad mínima de documentos por clase (minNc)")
    minNc = input();
    print("Ingrese la cantidad mínima de documentos por término (minNi)")
    minNi = input();
    print("Ingrese la cantidad de mejores términos que serán escogidos (numMejores)")
    numMejores = input();
    print("Ingrese un prefijo para usar en los nombres de los archivos generados")
    pref = input();
    pref=pref+"_"
    minNc=int(minNc)
    minNi=int(minNi)
    numMejores=int(numMejores)

    dictStopWords = {};
    numDocs={"num":0}
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
    first = [0,1]

    for i in first:
        if i == 0:
            # Se sacan primero las clases
            readText(dictClass, dictWords, dictStopWords, i, minNc,filepath, numDocs);
        else:
            readText(dictClass, dictWords, dictStopWords, i, minNc,filepath, numDocs);
    
    
    dictWords=cleanWords(dictWords, minNi);

    valor=numDocs.get("num")
    generalEntropy=totalEntropy(dictClass, valor);
    termEntropy(dictClass, dictWords, valor, minNi);

    IG(dictWords, generalEntropy);

    top=mejoresTerminos(numMejores,dictWords)

    writeClass(dictClass, minNc,pref);
    writeDicc(dictWords, minNi,pref);
    print("\n\n")
    writeGI(round(generalEntropy,4),dictWords,pref);
    writeBest(top,pref);



main();

