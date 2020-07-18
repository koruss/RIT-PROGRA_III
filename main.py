import re
import math

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

#def entropiaClases():



def readFile():
    f = open('reut2-001.sgm', 'r')
    data= f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll('TITLE')
    for content in contents:
        print (content.text)

    



def main():
    dictStopWords = {};
    # readStopWords(dictStopWords);
    number = "9,1651,6168,3216,3158,3216,316,4685.21651654"
    number1="7,030,000 asfd sfada,sfd a asdfas qwer 4654 13213 5613.16354 qwer w654 4re,wq6r ewqre,wq asdf 654 321 1521.146 adfas 4654,79865.465 64,64968,65321.163"
    new=removeComma(number1);
    print(new);






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

