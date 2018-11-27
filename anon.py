import pandas as pd
import csv 
import os
import hashlib
import random
import time
import math
import string
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
        
        month -> 12 , 01 , 02 ...,12
    """
    
    def __init__(self,pathFile):
        self.pathFile = pathFile
        self.matrice = []
        self.header = "" 
        self.monthIdxsList =[]
        self.userList=[]
        self.itemList=[]
        
    def load(self):
        mat = []
        month="01"
        index=0
        users=[]
        items=[]
        with open(self.pathFile) as file:
            reader = csv.reader(file,skipinitialspace=True, quotechar="'")
            for row in reader:                
                mat.append(row)
                monthTmp = row[1][5:7]
                users.append(row[0])
                items.append(row[3])
                if(monthTmp != month and index!=0):
                    self.monthIdxsList.append(index)
                    month = monthTmp
                index+=1
        self.userList=list(set(users))
        self.itemList=list(set(items))
        self.header = mat[:1][0]
        self.matrice = mat[1:]
                
                
    
    def deleteItemCategories(self):
        for line in self.matrice:
            line[3] = line[3][:5]
    
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
                    line[4] = _categories[catIndex]
                    break
                elif(float(line[4])>_categories[i]):
                    catIndex+=1
                if(i==len(_categories)-1):
                    line[4]=_categories[-1]
                
    def generalizeQuantity(self,_categories):
        """_categories is a list with the upper limit of each price category"""
        for line in self.matrice:
            catIndex = 0
            for i in range(len(_categories)):
                if(float(line[5])<_categories[i]):
                    line[5] = _categories[catIndex]
                    break
                elif(float(line[5])>_categories[i]):
                    catIndex+=1
                if(i==len(_categories)-1):
                    line[5]=_categories[-1]
                    
    def generalizeQuantityDizaine(self):
        """_categories is a list with the upper limit of each price category"""
        for line in self.matrice:
            line[5] = self.roundup(int(line[5]))
        

    def shuffle(self, list ):
        random.shuffle(list)
        return list
        
    def getSensitiveQuantity(self):
        print("[0-10,10-50,50-100,100-500,<500]")
        limits = [0,0,0,0,0]
        for line in self.matrice:
            qty = int(line[ -1])
            if(qty<=10):
                limits[0] = limits[0]+1
            elif(qty>10 and qty<=50):
                limits[1] = limits[1]+1
            elif(qty>50 and qty<=100):
                limits[2] = limits[2] +1
            elif(qty>100 and qty <=500):
                limits[3]  = limits[3] +1
            elif(qty>500):
                limits[4] = limits[4] +1 
        return limits
        
        
    def getSensitivePrice(self):
        print("[0-10,10-50,50-100,100-500,<500]")
        limits = [0,0,0,0,0]
        
        for line in self.matrice:
            qty = float(line[ -2])
            if(qty<=10):
                limits[0] = limits[0]+1
            elif(qty>10 and qty<=50):
                limits[1] = limits[1]+1
            elif(qty>50 and qty<=100):
                limits[2] = limits[2] +1
            elif(qty>100 and qty <=500):
                limits[3]  = limits[3] +1
            elif(qty>500):
                limits[4] = limits[4] +1 
        return limits
    
    
    def noiseSensitiveQuantity(self,borneMin,borneSup=math.inf):
        _qties=[0,5,10]
        for line in self.matrice:
            qty = int(line[ -1])
            if(qty>borneMin and qty<borneSup):
                line[-1] = random.choice(_qties)
        
        
    def noiseSensitivePrice(self,borneMin,borneSup=math.inf):
        _prices=[1,5,10,50]
        for line in self.matrice:
            qty = int(line[ -2])
            if(qty>borneMin and qty<borneSup):
                line[-2] = random.choice(_prices)
    
    
    
    def deleteSensitiveQuantity(self,borneMin,borneSup=math.inf):
        for line in self.matrice:
            qty = int(line[ -1])
            if(qty<borneMin or qty>borneSup):
                line[0] = "DEL"
        
    def deleteSensitivePrice(self,borneMin,borneSup=math.inf):
        for line in self.matrice:
            qty = float(line[ -2])
            if(qty<borneMin or qty>borneSup):
                line[0] = "DEL"
                
        
    def checkRedonAndDelete(self):
        l=[]
        x=0
        index=0
        indexstart=0
        month="12" 
        start = time.process_time()
        for line in self.matrice:
            monthTmp = line[1][-5:-3]
            if(month!=monthTmp):
                print("Temps d'changement d'idx : {}".format(time.process_time() - start))
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
        
    def createRandomLine(self,date):
        _prices=[1,5,10,50,100]
        _qties=[0,5,10,25]
        _hours=["10:00","14:00"]
        user_id = random.choice(self.userList)
        item_id = random.choice(self.itemList)
        return [user_id,date,random.choice(_hours),item_id,str(random.choice(_prices)),str(random.choice(_qties))]
        
    def getAllUserTotalItem(self):
        #Comment on peut attaquer un utilisateur plus facilement, avec un grand nombre d'achat ou un petit nombre d'achat 
        #TODO FAIRE une fonction qui recupere le nombre d'achat d'un utilisateur par MOIS
        usersList = [line[0] for line in self.matrice]
        resMatrix=[]
        f = open("userTotalItem.txt","w")
         
        for user in self.userList:
            f.write(str(user) + "-"+ str(usersList.count(user))+"\n")
        f.close()
        
    def getUserTotalItem(self,user):
        usersList = [line[0] for line in self.matrice]
        return usersList.count(user)
    
    
    def monthItemGathering(self):
        res=[]
        tmp=[]
        user_item_ids=[]
        item_id_counter=[]
        matrixIndex=[]
        timeNb=[]
        lxd=[]
        monthCounter=0
        delLine=0
        for line in self.matrice:
            tmp =[sum(bytearray(line[0],'utf8')),sum(bytearray(line[3],'utf8'))]
            if tmp not in user_item_ids:
                user_item_ids.append(tmp)
                item_id_counter.append(int(line[-1]))
                matrixIndex.append(monthCounter)
                timeNb.append(1)
                
            else:
                item_id_counter[user_item_ids.index(tmp)] =   item_id_counter[user_item_ids.index(tmp)] +int(line[-1])
                timeNb[user_item_ids.index(tmp)] +=1
                line[-1]=0
                delLine+=1
            monthCounter+=1
            if monthCounter in self.monthIdxsList[1:]:
                # res.append([[user_item_ids[x],item_id_counter[x]] for x in range(len(user_item_ids))])
                print("LENGTH OF THE INDEX MATRIX",len(matrixIndex))
                print("DELETED LINES : ",delLine)
                print("CURRENT INDEX : ", monthCounter)
        
        print("END OF INIT")
        for line in self.matrice:
            tmp =[sum(bytearray(line[0],'utf8')),sum(bytearray(line[3],'utf8'))]
            cnter=item_id_counter[user_item_ids.index(tmp)]
            time=timeNb[user_item_ids.index(tmp)]
            line[-1] = int(cnter/time)
                
 
        
        
    def getFinalUsers(self,borneInf, borneSup):
        finalUserList = []
        with open("userTotalItem.txt","r") as uFile:
            data = uFile.readlines()
            for line in data:
                user_id = line.split("-")[0]
                nb = int(line.split("-")[1])
                if nb<borneSup and nb>borneInf:
                    finalUserList.append(user_id)
        for line in self.matrice:
            if not line[0] in finalUserList:
                line[0] = "DEL"
                
    def roundup(self,x):
        return int(math.ceil(x / 10.0)) * 10
    
    def getNbSupOfUsers(self,borne):
        nb=[]
        with open("userTotalItem.txt","r") as uFile:
            data = uFile.readlines()
            for line in data : 
                nb.append(int(line.split("-")[1]))
        return sum(i>borne for i in nb)
    
    
    def getNbInfOfUsers(self,borne):
        nb=[]
        with open("userTotalItem.txt","r") as uFile:
            data = uFile.readlines()
            for line in data : 
                nb.append(int(line.split("-")[1]))
        return sum(i<borne for i in nb)
    
    
    def checkRedonAndNoise(self):
        l=[]
        x=0
        index=0
        indexstart=0
        month="12"
        start = time.process_time()
        for line in self.matrice:
            monthTmp = line[1][-5:-3]
            if(month!=monthTmp):
                # print("Temps d'changement d'idx : {}".format(time.process_time() - start))
                start = time.process_time()
                month=monthTmp
                # print("index change")
                # print("INDEX --> " ,index)
                l[:]=[]
            p = ''.join(list(map(str,line)))
            if(p not in l):
                l.append(p)
            else:
                line = self.createRandomLine(line[1])
                x+=1
            index+=1
        return x
                
                
                
    def getLength(self):
        return len(self.matrice)
    
    
    def deletedLines(self):
        counter=0
        for line in self.matrice:
            if "DEL" in line[0]:
                counter+=1
        return counter
    
    def getlinesIdUser(self,user):
        subMatrix = []
        for line in self.matrice:
            if(line[0]==user):
                subMatrix.append(line)
        return subMatrix
        
    def shuffleUsersPairs(self):
        userListShuffled = self.shuffle(self.userList)
        for idxLine in range(len(self.matrice)):
            user = self.matrice[idxLine][0]
            self.matrice[idxLine][0] = userListShuffled[self.userList.index(user)]
            
    def shuffleDateHoursPrice(self):
        hours = ["14:00","10:00"]
        price = [0,1]
        month = ["12"] + [str(x).zfill(2) for x in range(1,13)]
        for idxLine in range(len(self.matrice)):
            self.matrice[idxLine][2] = random.sample(hours,1)[0]
            self.matrice[idxLine][4] = random.sample(price,1)[0]
            self.matrice[idxLine][1] = self.matrice[idxLine][1][:5]+str(random.sample(month,1)[0])+self.matrice[idxLine][1][7:]

        
def routine():
    mat = matrix(P)
    mat.load()
    
    #vire les A-B-C dans les item_id
    # mat.deleteItemCategories()
    
    #Generalisation au Mois
    mat.generalizeMonth()
    
    #Generalisation de l'heure par période
    mat.generalizeDayPeriod()
    
    #on fait des truc avec les quantité trop chopable 
    m = mat.getSensitiveQuantity()
    print("sensitive qties :" ,m)
    
    #on fait des truc avec les prix trop chopable
    m = mat.getSensitivePrice()
    print("sensitive prices :" ,m) 
    
    #Generalisation du prix
    mat.generalizePrice([0,5,10,25,50,100,500])
    
    #Generalisation de la quantité
    # mat.generalizeQuantity([1,10,50,100,500,1000])
    mat.generalizeQuantityDizaine()
    
    #pseudonimiser les item id
    # mat.pseudonimazeItemId()
    
    #regrp le total des items par mois par user
    mat.monthItemGathering()
    
    # on mélange tout les users
    # print("SHUFFLE USERS")
    # mat.shuffleUsersPairs()
    
    print("SHUFFLE MONTH HOURS PRICE")
    mat.shuffleDateHoursPrice()
    
    # #pseudonimiser les user id
    # mat.pseudonimazeUserId()
    
    
    #del some users 
    # mat.getFinalUsers(10,80)
    

    #check les redondances et ajoute du bruits 
    # print("NUMBER OF DOUBLONS : " +str(mat.checkRedonAndDelete()))
    
    
    dLines = mat.deletedLines()
    print("NUMBER OF DELETED LINES : ", dLines)
    print(" DELETED LINES : " + str(dLines/mat.getLength()*100)[:4]+"%")
    
    print("SAUVEGARDE")
    mat.save("ouputTestprice.csv")
    
def mainQ():
    mat = matrix(P)
    mat.load()
   


def mainP():
    mat = matrix(P)
    mat.load()
    m = mat.getSensitivePrice()
    print("sensitive :" ,m)
    print("TOTAL DONE : ", sum(m))
    print("MATRIX LENGHT  : ", mat.getLength())



def main():
    print("DEBUT ANONYMISATION")
    start = time.process_time()
    routine()
    print("Temps d'anonymisation : {}".format(time.process_time() - start))
    

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
    
        
m = matrix(P)
m.load()
m.generalizeDayPeriod()
m.generalizeMonth()
        



    
