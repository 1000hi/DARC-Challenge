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
# P= "./data/submission.csv"
P= "./data/ground_truth.csv"
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
                row[0] = 'KAKKAKAK'+row[0]
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
    
    def cardinalDay(self,liste):
        days=[]
        counter_day=[]
        for line in liste:
            day = int(line[1][-2:])
            if day not in days:
                days.append(day)
                counter_day.append(1)
            else:
                counter_day[days.index(day)] = counter_day[days.index(day)] + 1
        # print(days)
        return sorted([[days[i],counter_day[i]] for i in range(len(days))],key=lambda day : day[1])
        
    def generalizeMonth(self):
        idxCounter = 2
        idxMountCounter = 0 
        self.monthIdxsList[0] = 0
        for idxMonth in range(len(self.monthIdxsList)-1):
            debIdx =self.monthIdxsList[idxMonth]
            finIdx = self.monthIdxsList[idxMonth+1]
            res =self.cardinalDay( self.matrice[debIdx:finIdx])
            # print(res)
            res = res[-(int(len(res)*0.35)):]
            # print(res)
            daysRes = [x[0] for x in res]
            for line in self.matrice[debIdx:finIdx]:
                day = int(line[1][-2:])
                if day not in daysRes:
                    line[1] = line[1][:-2]+str(res[-(day%len(res))][0]).zfill(2)
                    
            print("APRES COUP" ,self.cardinalDay( self.matrice[debIdx:finIdx]))
            # print(res)
            
            # day = int(line[1][-2:])
            # line[1] = line[1][:-2]+str(int(day/7)*7+1)
   
            
            
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
            # hours = line[2][:2]
            # line[2] = hours+":00"
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
                    
    def generalizeQuantity(self):
        """_categories is a list with the upper limit of each price category"""
        for line in self.matrice:
            line[5] = self.myround(int(line[5]))
    
    def generalizePriceRound(self):
        for line in self.matrice:
            line[4] = round(float(line[4]),1)
        

    def shuffle(self, list ):
        random.shuffle(list)
        return list
    
    
    def myround(self,x, base=5):
        return int(base * round(float(x)/base))
    
    def cardinalQties(self):
        qties=[]
        counter_qties=[]
        for line in self.matrice:
            qty = int(line[-1])
            if qty not in qties:
                qties.append(qty)
                counter_qties.append(1)
            else:
                counter_qties[qties.index(qty)] = counter_qties[qties.index(qty)] + 1
        return sorted([[qties[i],counter_qties[i]] for i in range(len(qties))],key=lambda qty : qty[1])
        
    def cardinalPrice(self):
        price=[]
        counter_price=[]
        for line in self.matrice:
            pr = float(line[-2])
            if pr not in price:
                price.append(pr)
                counter_price.append(1)
            else:
                counter_price[price.index(pr)] = counter_price[price.index(pr)] + 1
        return sorted([[price[i],counter_price[i]] for i in range(len(price))],key=lambda pr : pr[1])
    
    def cardinalHours(self):
        hours=[]
        counter_hours=[]
        for line in self.matrice:
            hour = int(line[2][:2])
            if hour not in hours:
                hours.append(hour)
                counter_hours.append(1)
            else:
                counter_hours[hours.index(hour)] = counter_hours[hours.index(hour)] + 1
        return sorted([[hours[i],counter_hours[i]] for i in range(len(hours))],key=lambda hour : hour[0])
    
        
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
        
        
    def noiseSensitivePrice(self,listOfQty):
        for line in self.matrice:
            if(float(line[-2])) in listOfQty:
                # line[-1] = self.myround(float(line[-1]),12)
                line[-2] = int(float(line[-2]))
                line[0] = "DEL"
    
    def deleteListOfSensitiveQuantity(self, listOfQty):
        for line in self.matrice:
            if(int(line[-1])) in listOfQty:
                # line[-1] = self.myround(float(line[-1]),12)
                line[0] ="DEL"
                
    
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
                res.append([[user_item_ids[x],item_id_counter[x]] for x in range(len(user_item_ids))])
                print("LENGTH OF THE INDEX MATRIX",len(matrixIndex))
                print("DELETED LINES : ",delLine)
                print("CURRENT INDEX : ", monthCounter)
    
        for line in self.matrice:
            tmp =[sum(bytearray(line[0],'utf8')),sum(bytearray(line[3],'utf8'))]
            cnter=item_id_counter[user_item_ids.index(tmp)]
            time=timeNb[user_item_ids.index(tmp)]
            line[-1] = self.myround(int(cnter/time),12)
    
    
    
    
    
        
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
            
            
    def shuffleItemPairs(self):
        itemListShuffled = self.shuffle(self.itemList)
        for idxLine in range(len(self.matrice)):
            item = self.matrice[idxLine][3]
            self.matrice[idxLine][3] = itemListShuffled[self.itemList.index(item)]
            
    def shuffleDateHours(self):
        hours = ["14:00","10:00"]
        month = ["12"] + [str(x).zfill(2) for x in range(1,13)]
        for idxLine in range(len(self.matrice)):
            self.matrice[idxLine][2] = str(random.randint(1,10)).zfill(2)+":00"
            self.matrice[idxLine][1] = self.matrice[idxLine][1][:5]+str(random.sample(month,1)[0])+self.matrice[idxLine][1][7:]
    def lilCobain(self,nb):
        id=0
        for idx in range(len(self.monthIdxsList)-1):
            for x in range(nb):
                self.matrice[random.randint(self.monthIdxsList[idx],self.monthIdxsList[idx+1])][0] = "DEL"
        
def routine():
    mat = matrix(P)
    mat.load()
    
    #vire les A-B-C dans les item_id
    # mat.deleteItemCategories()
    

    print('Generalisation au Mois')
    mat.generalizeMonth()
    
    print("Generalisation de l'heure par période")
    mat.generalizeDayPeriod()
    
    #on fait des truc avec les quantité trop chopable 
    m = mat.getSensitiveQuantity()
    print("sensitive qties :" ,m)
    
    #on fait des truc avec les prix trop chopable
    m = mat.getSensitivePrice()
    print("sensitive prices :" ,m) 
    
    #Generalisation du prix
    # mat.generalizePrice([0,5,10,25,50,100,500])
    mat.generalizePriceRound()
    
    # print('Generalisation de la quantité')q
    # mat.generalizeQuantity([1,10,50,100,500,1000])
    # mat.generalizeQuantity()
    
    #pseudonimiser les item id
    # mat.pseudonimazeItemId()
    
    #regrp le total des items par mois par user
    # mat.monthItemGathering()
    
    # on mélange tout les users
    print("SHUFFLE USERS")
    mat.shuffleUsersPairs()
     
    print("SHUFFLE ITEM")    
    mat.shuffleItemPairs()
    
    l= mat.cardinalQties()
    limSup = 100
    badQties = [l[i][0] for i in range(len(l)) if l[i][1]<=limSup]
    print("HIDE SENSITIVE QTY : ",limSup)
    mat.deleteListOfSensitiveQuantity(badQties)
    
    
    
    
    l=mat.cardinalPrice()
    limSup = 2500
    badPrice = [l[i][0] for i in range(len(l)) if l[i][1]<=limSup]
    print("HIDE SENSITIVE PRICE  : ",limSup)
    mat.noiseSensitivePrice(badPrice)
    
    
    print("SHUFFLE MONTH HOURS ")
    mat.shuffleDateHours()
    
    # #pseudonimiser les user id
    # mat.pseudonimazeUserId()
    
    
    #del some users 
    # print("FINAL USERS")
    # mat.getFinalUsers(5,90)
    

    #check les redondances et ajoute du bruits 
    # print("TCHEK DOUBLONS AND DEL")
    # print("NUMBER OF DOUBLONS : " +str(mat.checkRedonAndDelete()))
    
    
    mat.lilCobain(50)
    
    dLines = mat.deletedLines()
    print("NUMBER OF DELETED LINES : ", dLines)
    print(" DELETED LINES : " + str(dLines/mat.getLength()*100)[:4]+"%")
    
    print("SAUVEGARDE")
    mat.save("ouput.csv")
    
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
# BEGGININNG OF MAIN TEST 
# Temps de lecture : 0.5
# Temps d'initialisation : 0.203125
# E1 score : 0.6972675019267774
# E2 score : 0.6603458611710322
# E3 score : 0.5354496037955323
# E4 score : 0.0
# E5 score : 0.0
# E6 score : 0.0
# Temps de calcul : 452.625
# Temps d'initialisation : 35.34375
# S1 score : 0.150552
# S2 score : 0.039162
# S3 score : 0.16794
# S4 score : 0.593923
# S5 score : 0.197189
# S6 score : 0.659327
# Temps de calcul : 29.203125
# Temps de calcul TOTAL : 517.875


# BEGGININNG OF MAIN TEST 
# Temps de lecture : 0.53125
# Temps d'initialisation : 0.265625
# E4 score : 0.1666682237
# E5 score : 0.0483248711
# E6 score : 0.1081
# Temps de calcul : 29.1875
# Temps d'initialisation : 63.015625
# S1 score : 0.035304
# S2 score : 0.017544
# S3 score : 0.173489
# S4 score : 0.197747
# S5 score : 0.063028
# S6 score : 0.089669
# Temps de calcul : 28.953125
# Temps de calcul TOTAL : 121.953125
    
        
m = matrix(P)
m.load()
# # m.generalizeDayPeriod()
# m.generalizeMonth()
# m.monthItemGathering()
        


if __name__ == "__main__":
    main()
    mainTest()

    
