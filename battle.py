'battle.py'
from time import sleep as sl
import sys
import csv
from copy import copy
import random
#print(sys.version)

class battle:

    def __init__(self, army1, army2, stats, terain):
        print(terain)
        self.army1=army1
        self.army2=army2
        self.stats=stats
        self.fight()

    def check_ranged(self, army, fight):
        try:
            if army[2][1]=="arch" or army[2][1]=="art":
                fight[2]=army[2]
        except KeyError:
            pass
        try:
            if army[3][1]=="art":
                fight[3]=army[3]
        except KeyError:
            pass#'''
        return fight

    def fight(self): #Initiates armyies
        self.won=False
        self.army1_out=[] #The value that is returned, after bsttle, only the units thst lost
        self.army2_out=[]
        while len(self.army1)!=0 and len(self.army2)!=0:
            #print(self.army1)
            #print(self.army2)
            army1={}
            army2={}
            for i in range(1, len(self.army1)+1):
                #Assignes each unit to a line (key), value 1 is level*amount, value 2 is unit name
                army1[i]=[self.army1[i][0]*(1+self.army1[i][1]/100), self.army1[i][2]]
            for i in range(1, len(self.army2)+1):
                army2[i]=[self.army2[i][0]*(1+self.army2[i][1]/100), self.army2[i][2]]
            print("dhs", army1)
            print(self.army1, type(self.army1))

            #Initiates the army that will deal and take damage
            fight_army1={1:army1[1]}
            fight_army2={1:army2[1]}
            print(fight_army1)

            #Checks are there any reange units and if so adds its damage and morale damage
            fight_army1=self.check_ranged(army1, fight_army1)
            fight_army1=self.check_ranged(army2, fight_army2)

            self.single_battle_prep(fight_army1, fight_army2)
            #print(self.army2)
            print("\n\n_____________________________________________________________________________________________________________\n\n")
        #print(self.army1, self.army1_out)
        #print("\n\n")
        #print(self.army2, self.army2_out)
        #print()

    def single_battle_prep(self, army1, army2):
        print("army1:", army1)
        print("army2:", army2)
        current1={"health":0, "morale":0, "damage":0, "morale_damage":0}
        current2={"health":0, "morale":0, "damage":0, "morale_damage":0}

        current1["health"]=float(army1[1][0])*float(self.stats[army1[1][1]][0])
        current2["health"]=float(army2[1][0])*float(self.stats[army2[1][1]][0])

        current1["morale"]=float(army1[1][0])*float(self.stats[army1[1][1]][1])
        current2["morale"]=float(army2[1][0])*float(self.stats[army2[1][1]][1])

        for unit in army1:
            current1["damage"]+=float(army1[unit][0])*float(self.stats[army1[unit][1]][2])/float(unit)
        for unit in army2:
            current2["damage"]+=float(army2[unit][0])*float(self.stats[army2[unit][1]][2])/float(unit)

        for unit in army1:
            current1["morale_damage"]+=float(army1[unit][0])*float(self.stats[army1[unit][1]][3])/float(unit)
        for unit in army2:
            current2["morale_damage"]+=float(army2[unit][0])*float(self.stats[army2[unit][1]][3])/float(unit)

        if army2[1][1] in ["arch", "art"]:
            #print(current2)
            new1, new2, win=self.single_battle(current1, current2, army1)
            print("attacke", win)
            self.won=win
            #print(current2)
            #print(new1==current1)
        elif army1[1][1] in ["arch", "art"]:
            new2, new1, win=self.single_battle(current2, current1, army2)
            print("defender", win)
            self.won=not(win)
        elif self.won==False:
            new1, new2, win=self.single_battle(current1, current2, army1)
            print("attacke", win)
            self.won=win
        else:
            new2, new1, win=self.single_battle(current2, current1, army2)
            print("defender", win)
            self.won=not(win)
        #print(army1[1][1], army2[1][1])
        #print(current1, current2, self.army1, self.army2)
        try:
            self.army1[1][0]=self.army1[1][0]*(new1["health"]/current1["health"])
        except ZeroDivisionError:
            self.army1[1][0]=self.army1[1][0]*0
        #self.army1[1][0]=self.army1[1][0]*(new1["morale"]/current1["morale"])
        try:
            self.army2[1][0]=self.army2[1][0]*(new2["health"]/current2["health"])
        except ZeroDivisionError:
            self.army2[1][0]=0
        #self.army2[1][0]=self.army2[1][0]*(new1["morale"]/current1["morale"])
        '''print("new1:", new1)
        print("current1:", current1)
        print("army1:", self.army1)
        print("new2:", new2)
        print("current2:", current2)
        print("army2:", self.army2)'''
        #print(new1["health"]/current1["health"])

        if  new1["health"]<=0 or new1["morale"]<=0:
            lis=list(self.army1.keys())
            lis.sort()
            for i in lis:
                self.army1[i-1]=self.army1[i]
            if new1["health"]>0:
                self.army1[0][0]=round(self.army1[0][0], 1)
                self.army1_out.append(self.army1[0])
            self.army1.pop(i)
            self.army1.pop(0)
            del(lis)

        if  new2["health"]<=0 or new2["morale"]<=0:
            lis=list(self.army2.keys())
            lis.sort()
            for i in lis:
                self.army2[i-1]=self.army2[i]
            if new2["health"]>0:
                self.army2[0][0]=round(self.army2[0][0], 1)
                self.army2_out.append(self.army2[0])
            self.army2.pop(i)
            self.army2.pop(0)
            del(lis)

    def single_battle(self, current1, current2, armya):
        currenta=copy(current1)
        currentd=copy(current2)
        print("currenta:", currenta)
        print("currentd:", currentd)#'''
        #print(armya)
        if 0>=currentd["morale"]:
            return currenta, currentd, False
        elif 0>=currenta["morale"]:
            return currenta, currentd, True
        if armya[1][1]=="cav":
            #print("charge")
            currenta["morale_damage"]=currenta["morale_damage"]*1.75
            currentd["damage"]=currentd["damage"]/1.75
        else:
            pass
        while True:
            currentd["morale"]-=(currenta["morale_damage"]/1000)*random.randint(5, 15)/100
            if 0>=currentd["morale"]:
                return currenta, currentd, True
            currentd["health"]-=(currenta["damage"]/1000)*random.randint(5, 15)/100
            if 0>=currentd["health"]:
                return currenta, currentd, True
            currenta["morale"]-=(currentd["morale_damage"]/1000)*random.randint(5, 15)/100
            if 0>=currenta["morale"]:
                return currenta, currentd, False
            currenta["health"]-=(currentd["damage"]/1000)*random.randint(5, 15)/100
            if 0>=currentd["health"]:
                return currenta, currentd, False

def unit(unit, pos, max):
    st=(unit+" :")
    unit=proper_input(st)
    unit_xp=proper_input("xp: ")
    unit_pla=proper_input("place: ", ubound=max, used=pos)
    if unit!=0:
        pos.append(unit_pla)
    else:
        max-=1
    return unit, unit_xp, unit_pla, pos, max

def army(who):
    pos=[]
    max=4
    '''
    sol, sol_xp, sol_pla, pos, max=unit("Soldiers", pos, max)
    arch, arch_xp, arch_pla, pos, max=unit("Archer", pos, max)
    cav, cav_xp, cav_pla, pos, max=unit("Cavalery", pos, max)
    art, art_xp, art_pla, pos, max=unit("Artillery", pos, max)
    '''
    if who==True:
        sol, sol_xp, sol_pla=0,1,2
        arch, arch_xp, arch_pla=0,1,3
        cav, cav_xp, cav_pla=30,100,1
        art, art_xp, art_pla=0,1,4
    else:
        sol, sol_xp, sol_pla=2,75,1
        arch, arch_xp, arch_pla=1,1,2
        cav, cav_xp, cav_pla=0,1,4
        art, art_xp, art_pla=1,1,3
    #'''
    army_dic={
        sol_pla:[sol, sol_xp, "sol"],
        arch_pla:[arch, arch_xp, "arch"],
        cav_pla:[cav, cav_xp, "cav"],
        art_pla:[art, art_xp, "art"]
        }
    return army_dic

def proper_input(text, ubound=None, used=None):
    while True:
        try:
            out=int(input(text))
            if ubound!=None:
                if out>ubound:
                    print("Try that again")
                    continue
            if used!=None and used!=[]:
                if out in used:
                    print("Try that again")
                    continue
            return out
        except ValueError:
            print("Try that again")

def read_stats():
    stats=open("info/army.csv", "r")
    lis={}
    for i in range(4):
        stat=stats.readline()
        stat=stat.split(",")
        lis[stat[0]]=stat[1:-1]

    stats.close()
    return lis

def analize_stats(army1, army2):
    print(army1, army2)
    sol, sol_xp, sol_pla=army1[0], army1[1], army1[2]
    arch, arch_xp, arch_pla=army1[3], army1[4], army1[5]
    cav, cav_xp, cav_pla=army1[6], army1[7], army1[8]
    art, art_xp, art_pla=army1[9], army1[10], army1[11]
    check=[sol_pla, arch_pla, cav_pla, art_pla]
    if len(check)==len(set(check)):
        pass
    else:
        return ["lol wrong position"]

    army_dic1={
        sol_pla:[sol, sol_xp, "sol"],
        arch_pla:[arch, arch_xp, "arch"],
        cav_pla:[cav, cav_xp, "cav"],
        art_pla:[art, art_xp, "art"]
        }

    #print(army_dic1.keys())
    for key in army_dic1.keys():
        if 0<key<5 and 0<army_dic1[key][1]<101:
            pass
        else:
            return ["lol wrong values"]

    sol, sol_xp, sol_pla=army2[0], army2[1], army2[2]
    arch, arch_xp, arch_pla=army2[3], army2[4], army2[5]
    cav, cav_xp, cav_pla=army2[6], army2[7], army2[8]
    art, art_xp, art_pla=army2[9], army2[10], army2[11]
    check=[sol_pla, arch_pla, cav_pla, art_pla]
    if len(check)==len(set(check)):
        pass
    else:
        return ["lol wrong position"]

    army_dic2={
        sol_pla:[sol, sol_xp, "sol"],
        arch_pla:[arch, arch_xp, "arch"],
        cav_pla:[cav, cav_xp, "cav"],
        art_pla:[art, art_xp, "art"]
        }

    for key in army_dic2.keys():
        if 0<key<5 and 0<army_dic2[key][1]<101:
            pass
        else:
            #print("here")
            return ["lol wrong values"]
    result=main(army1=army_dic1, army2=army_dic2)
    #print(result)
    #print(result)
    #print(type(result))
    return result

def main(army1=None, army2=None):
    stats=read_stats()

    if army1==None or army2==None:
        army1=army(True)
        army2=army(False)
    else:
        pass
    terain=None

    battle1=battle(army1, army2, stats, terain)

    if len(list(battle1.army1.keys()))==0:
        win="Defender won"
        for unit in battle1.army2.keys():
            #print(battle1.army2[unit])
            battle1.army2[unit][0]=round(battle1.army2[unit][0], 1)
            #print(battle1.army2[unit])
    else:
        win="Attacker won"
        for unit in battle1.army1.keys():
            battle1.army1[unit][0]=round(battle1.army1[unit][0], 1)

    army1_surv=list(battle1.army1.values())+battle1.army1_out
    army2_surv=list(battle1.army2.values())+battle1.army2_out

    #return win
    return [win, army1_surv, army2_surv]

if __name__=="__main__":
    '''wins={"a":0, "d":0}
    for i in range(100):
        win=main()
        if win=="Defender won":
            wins["d"]+=1
        elif win=="Attacker won":
            wins["a"]+=1
        else:
            print("retardation")
            break#'''
    lols=main()
    #print(lols)
    for lol in lols:
        print(lol)#'''
#print(wins)
