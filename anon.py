import pandas as pd
import csv 
import os
import hashlib
import random


os.chdir("C:\\Users\\Milly\\DARC-Challenge")

# Path to the csv
P= "./data/submission.csv"
#id_user|date|hours|id_item|price|qty


class matrix():
    """ 
        line [0] -> id user
        line [1] -> date
        line [2] -> hours
        line [3] -> id_item
        line [4] -> price
        line [5] -> quantity 
    """
    
    def __init__(self,pathFile):
        self.pathFile = pathFile
        self.matrice = []
        self.header = "" 
        self.dayIdxsList =[]
        
    def load(self):
        mat = []
        day="01"
        index=0
        with open(self.pathFile) as file:
            reader = csv.reader(file,skipinitialspace=True, quotechar="'")
            for row in reader:                
                mat.append(row)
                dayTmp = row[1][-2:]
                if(dayTmp != day and index!=0):
                    self.dayIdxsList.append(index)
                    day = dayTmp
                index+=1
        self.header = mat[:1][0]
        self.matrice = mat[1:]
                
                
                
    def readableSave(self,outputFileName):
        with open(outputFileName, 'w') as csvfile:
            spamwriter = csv.writer(csvfile,  delimiter=';', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
            spamwriter.writerow("id_user|date|hours|id_item|price|qty")
            for line in self.matrice:
                spamwriter.writerow(line)
                
    def save(self,outputFileName):
        with open(outputFileName, 'w') as csvfile:
            spamwriter = csv.writer(csvfile,  delimiter=',',lineterminator = '\n')
            spamwriter.writerow(["id_user","date","hours","id_item","price","qty"])
            for line in self.matrice:
                spamwriter.writerow(line)
    
    def pseudonimazeUserId(self):
        """use sha224 to hide real id """
        for line in self.matrice:
            line[0] = hashlib.sha224(line[0].encode('utf-8')).hexdigest()
    
    def pseudonimazeItemId(self):
        """use sha224 to hide real id """
        for line in self.matrice:
            line[3] = hashlib.sha224(line[3].encode('utf-8')).hexdigest()
            
    def generalizeWeek(self):
        for line in self.matrice:
            week = str((31%7 - (int(line[1][-2:])-1)%7)*7-1).zfill(2)
            line[1] = line[1][:-2] + week
            
        
    def generalizeMonth(self):
        for line in self.matrice:
            line[1] = line[1][:-2]+"01"
            
    def generalizeDayPeriod(self):
        """
        only display : 
        - morning ->   06:00<hours<12:00 
        - afternoon -> 12:00<hours 
        will display : 
        - 10:00 for morning
        - 14:00 for afternoon 
        """
        for line in self.matrice:
            hours = int(line[2][:2])
            if(hours<12):
                line[2] = "10:00"
            else:
                line[2] = "14:00"
                
    def generalizePrice(self,_categories):
        """_categories is a list with the upper limit of each price category"""
        for line in self.matrice:
            catIndex = 0
            for i in range(len(_categories)):
                if(float(line[4])<_categories[i]):
                    line[4]=_categories[catIndex]
                else:
                    catIndex+=1
                
    def generalizeQuantity(self,_categories):
        """_categories is a list with the upper limit of each price category"""
        for line in self.matrice:
            catIndex = 0
            for i in range(len(_categories)):
                if(float(line[5])<_categories[i]):
                    line[5]=_categories[catIndex]
                else:
                    catIndex+=1
    def shuffle(self):
        random.shuffle(self.matrice)
        
    def checkRedon(self):
        self.matrice.insert(2,self.matrice[2])
        self.matrice.insert(2,self.matrice[2])
        self.matrice.insert(45,self.matrice[45])
        self.matrice.insert(564,self.matrice[564])
        l=[]
        x=0
        index=0
        indexstart=0
        month="12"
        start = time.process_time()
        for line in self.matrice:
            monthTmp = line[1][-5:-3]
            if(month!=monthTmp):
                print("Temps d'changement idx : {}".format(time.process_time() - start))
                start = time.process_time()
                month=monthTmp
                print("index change")
                print("INDEX --> " ,index)
                l[:]=[]
            p = ''.join(list(map(str,line)))
            if(p not in l):
                l.append(p)
            else:
                line[0] = "DEL"
                x+=1
            index+=1
        return x
                
                
                
                
        
            
        
def main():
    mat = matrix(P)
    mat.load()
    mat.pseudonimazeItemId()
    mat.generalizeMonth()
    mat.generalizeDayPeriod()
    mat.generalizePrice([0,5,10,25])
    mat.generalizeQuantity([1,5,10,50,100])
    print("NUMBER OF DOUBLONS : " +str(mat.checkRedon()))
    mat.save("ouputTestprice.csv")
    




#Run for the ./data/submission.csv
# Temps de lecture : 0.6875
# Temps d'initialisation : 0.25
# E1 score : 0.6972675019267774
# E2 score : 0.6603458611710322
# E3 score : 0.5354496037955323
# E4 score : 0.0
# E5 score : 0.9107717048
# E6 score : 0.0
# Temps de calcul : 501.484375
# Temps d'initialisation : 43.625
# S1 score : 0.785054
# S2 score : 0.751011
# S3 score : 0.788623
# S4 score : 0.897004
# S5 score : 0.758583
# S6 score : 0.814084
# Temps de calcul : 33.140625
# Temps de calcul TOTAL : 579.1875
    

        




    
