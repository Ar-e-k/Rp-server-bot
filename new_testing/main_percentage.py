import csv
from copy import copy

class country:

    def __init__(self, name, overwrite, economy, expenses, army, education, manuals, manuals2, public):
        self.actual_income=0
        self.stablility_change=None
        self.literacy_change=None

        self.admin_manuals=manuals
        self.user_manuals=manuals2
        self.admin_manuals.update(self.user_manuals)
        all=self.read_stats("World_priv.csv")
        self.name=name
        #print(self.name)
        all=all[self.name]
        self.basics={}
        self.create_dic(self.basics, overwrite, all)
        self.economy={}
        self.economy["Pop_ratio"]={"Rpop":0, "Ipop":0, "Unemployed":0, "Young":0, "Army":0}
        self.create_dic(self.economy, economy, all)
        self.expenses={}
        self.create_dic(self.expenses, expenses, all)
        self.education={}
        self.create_dic(self.education, education, all)
        self.public={}
        self.create_dic(self.public, public, all)
        units=all["Army"][0:-1]
        #print(units)
        army_new=units.split(",")
        #print(army_new)
        for unit in range(0, 5):
            #print(self.army_new["Army"][unit])
            #print(army_new[unit])
            army_new[unit]=army_new[unit][2:-1]
        ships=all["Navy"][0:-1]
        #print(ships)
        navy_new=ships.split(",")
        for unit in range(0, 3):
            #print(self.army_new["Army"][unit])
            #print(army_new[unit])
            navy_new[unit]=navy_new[unit][2:-1]
        #print(army_new)
        #print(navy_new)
        self.army_new={"Army":dict(zip(["SOL", "ARCH", "CAV", "ART", "CON"], army_new)), "Navy":dict(zip(["LIGH", "HEAV", "BORD"], navy_new))}
        #print(self.army_new)
        self.all=[self.basics, self.economy, self.expenses, self.education, self.public, self.army_new]
        self.army=army
        #print(self.basics)

        self.tiers=self.read_stats("economy.csv")
        self.military_pay=self.read_stats('army_expences.csv')

        #print(self.tiers)
        #print(self.stability_tiers)
        #print(self.economy)
        #print(self.public)
        #print(self.tiers)
        self.stability_tiers=self.read_stats("stability.csv")

    def wierd(self):
        all=self.read_stats("World_priv.csv")
        all=all[self.name]
        for i in list(self.admin_manuals.keys()):
            all.pop(i)
        for cat in self.all:
            for key in cat.keys():
                if key in all:
                    self.all[self.all.index(cat)][key]=all[key]
                else:
                    pass

    #Passive tools
    def read_stats(self, name):
        with open("info/"+name) as file:
            values=[]
            reader=csv.reader(file)
            for line in reader:
                values.append(line)
        heads=values[0]
        values.pop(0)
        prop_values={}
        for value in values:
            prop_value=dict(zip(heads[1:], value[1:]))
            prop_values[value[0].upper()]=prop_value
        return prop_values

    def write_stats(self, fname, new):
        with open("info/"+fname, "w") as file:
            writer=csv.writer(file)
            writer.writerows(new)

    def edit_stats(self, fname):
        country, new=self.get_all(fname)
        new_list=[]
        new_dic={}
        name=self.name_capital()
        for line in self.all:
            a=new_dic.update(line)
        for head in new[0][1:]:
            if head=="Army":
                new_list.append(list(new_dic[head].values()))
                continue
            elif head=="Navy":
                new_list.append(list(new_dic[head].values()))
                continue
            new_list.append(new_dic[head])
        new_list.insert(0, name)
        new[country]=new_list
        self.write_stats(fname, new)

    def edit_stats_value(self, fname, value, source):
        country, new=self.get_all(fname)
        source=new[0].index(source)
        new[country][source]=value
        self.write_stats(fname, new)

    def name_capital(self):
        name=self.name.lower()
        name=list(name)
        name[0]=name[0].upper()
        if " " in name:
            for pos in range(0, len(name)-1):
                try:
                    if name[pos]==" " and name[pos+1]!="o":
                        name[pos+1]=name[pos+1].upper()
                    else:
                        pass
                except IndexError:
                    pass
        name="".join(name)
        return name

    def edit_name(self, fname, value):
        discordbet="qwertyuiopasdfghjklzxcvbnm-£1234567890"
        country, new=self.get_all(fname)
        for letter in value.lower():
            if letter in discordbet:
                pass
            else:
                return "Invalid character"
        self.name=value.upper()
        value=self.name_capital()
        new[country][0]=value
        self.write_stats(fname, new)
        return value

    def create_dic(self, dic, keys, source):
        for key in keys:
            dic[key]=source[key]
    #End of tools

    #Updating stuff
    def update_save(self):
        error=self.update_budget()
        if error==None:
            pass
        else:
            return error
        self.edit_stats("World_priv.csv")
        return None

    def update_budget(self): #Updates the overall country budget
        self.update_income()
        self.economy["Budget"]=float(self.economy["Budget"])+self.actual_income
        return self.check_budget()

    def check_budget(self):
        if self.economy["Budget"]<=0:
            if self.actual_income<0:
                text=self.name+" is out of budget, please contact them to limit spendings or get a loan\nThey currently need "+str(self.economy["Budget"])+" more money"
                self.wierd()
                return text
            else:
                print("interesting (its a bug)")

    def update_income(self): #Updates the actual income of the country
        self.update_stability()
        self.update_expenses()
        self.actual_income=self.get_actual_income()

    def update_per_income(self): #Updates income per Rural and Artisan population
        self.update_ratio()
        self.incomes={}
        self.incomes["Rural"]=self.get_income_class("Rural", "Rpop")
        self.incomes["Artisan"]=self.get_income_class("Artisan", "Ipop")

    def update_expenses(self): #Updates country spendings
        print(self.name)
        self.expense=0
        self.bill_army()
        #print(self.expenses)
        #print("work")
        self.expenses["army"]=int(self.army_pay)
        #print(self.navy_pay)
        self.expenses["navy"]=int(self.navy_pay)
        self.expenses["land"]=int(float(self.public["Area"])*float(self.tiers[self.economy["Economy_tier"].upper()]["Cost"]))
        self.expense+=self.get_expenses()
        print(self.expenses)

    def update_stability(self): #Updates stablility
        self.update_literacy()
        self.update_per_income()
        self.income=self.get_income()
        avarage_pay=self.get_avarage_pay()
        avarage_ben=self.get_avarage_ben()
        modifier=self.get_stab_mod(avarage_ben+avarage_pay)
        if modifier>0:
            self.stablility_change="Positive"
        elif modifier<0:
            self.stablility_change="Negative"
        else:
            self.stablility_change=None
        self.basics["Stability"]=float(self.basics["Stability"])+modifier
        self.basics["Stability"]=self.get_round(100, 0, self.basics["Stability"])

    def update_literacy(self): #Updates literacy, the amount of people in the country that are able to read&write
        spending=float(self.expenses["Technology_spending"])/float(self.basics["Population"])
        change=-(1-spending)
        if change>0:
            self.literacy_change="Positive"
        elif change<0:
            self.literacy_change="Negative"
        else:
            self.literacy_change=None
        self.education["Literacy"]=change/(10*float(self.education["Literacy"]))+float(self.education["Literacy"])
        self.education["Literacy"]=self.get_round(100, 0, self.education["Literacy"])

    def update_ratio(self): #Updates the amount of each group of people in the society
        self.economy["Pop_ratio"]["Young"]=self.get_young()
        self.economy["Pop_ratio"]["Army"]=self.get_manpower()
        rest_pop=float(self.basics["Population"])-(self.economy["Pop_ratio"]["Army"]+self.economy["Pop_ratio"]["Young"])
        employment=0
        for clas in ["Rpop", "Ipop"]:
            employment+=self.get_employed(rest_pop, clas)
        unemployed=rest_pop-employment
        self.economy["Pop_ratio"]["Unemployed"]=unemployed
        #print(self.economy)
    #End of updating stuff

    #Commands
    def change_name(self, value):
        value=self.edit_name("World_priv.csv", value)
        if value not in ["Invalid character"]:
            task="Task successfull\nYour new name is "+self.name
        else:
            task=value
        return task

    def change(self, source, value, admin=False):
        if admin==True:
            manuals=self.admin_manuals
        else:
            manuals=self.user_manuals
        if source in manuals.keys():
            pass
        else:
            return "Invalid source"
        try:
            if manuals[source][0]==int:
                value=manuals[source][0](float(value))
            else:
                value=float(value)
        except ValueError:
            pass
        if type(value)==manuals[source][0]:
            if None in manuals[source][1]:
                pass
            else:
                if type(value)==str:
                    if value in manuals[source][1]:
                        pass
                    else:
                        text1=",".join(manuals[source][1])
                        text="Invalid value, has to be one of the below\n"+text1
                        return text
                elif type(value)==float or type(value)==int:
                    if value>manuals[source][1][0] and value<manuals[source][1][1]:
                        pass
                    else:
                        text1=",".join([str(element) for element in manuals[source][1]])
                        text="Invalid value, has to be between: "+text1
                        return text
                else:
                    return "Something went wrong"
        else:
            text="Invalid value type, it should be "+str(manuals[source][0])[8:-2]+" type"
            return text
        for cat in self.all:
            if source in cat.keys():
                cat[source]=value
        #self.edit_stats_value("World_priv.csv", value, source)
        return "Task sucessfull"

    def change_army(self, value, unit, type):
        try:
            int(float(value))
        except ValueError:
            return "Invalid value"
        self.army_new[type][unit]=value
        return "Task successfull"

    def add(self, source, value, admin=False):
        if admin==True:
            manuals=self.admin_manuals
        else:
            manuals=self.user_manuals
        if source in manuals.keys():
            pass
        else:
            return "Invalid source"
        manuals2=manuals.copy()
        for key in manuals2.keys():
            if manuals[key][0] in [int, float]:
                pass
            else:
                del manuals[key]
        try:
            #print(manulas[source][0])
            value=manuals[source][0](value)
        except ValueError:
            return "Bad value"
        #print(val)
        for cat in self.all:
            if source in cat.keys():
                cat[source]=manuals[source][0](cat[source])+value
        #self.edit_stats_value("World_priv.csv", value, source)
        return "Task sucessfull"

    def add_army(self, value, unit, type):
        try:
            value=int(float(value))
        except ValueError:
            return "Invalid value"
        self.army_new[type][unit]=int(self.army_new[type][unit])+value
        return "Task successfull"

    def return_priv(self):
        print(self.all)
        print(self.expenses)
        priv=[
            "Budget",
            "Pop_ratio",
            "Tax_rate",
            "Technology_spending",
            "Building_spending",
            "Benefits_spending",
            "Economy_spending",
            "Army",
            "Navy"
            ]
        if int(self.economy["Trade"])>50:
            level=self.get_estimate(80, 60, self.economy["Trade"], "Monopoly", "Medium", "High")
        else:
            level=self.get_estimate(40, 20, self.economy["Trade"], "Medium", "None", "Low")
        #print(level)
        new_dic={"Trade":level}
        new_dic["Last income"]=self.actual_income
        level=self.get_estimate(65, 35, self.basics["Stability"], "High", "Low", "Mid")
        new_dic["Stability"]=level
        new_dic["Stablility_change"]=self.stablility_change
        level=self.get_estimate(65, 35, self.education["Literacy"], "High", "Low", "Mid")
        new_dic["Literacy"]=level
        new_dic["Literacy_change"]=self.literacy_change
        #print(new_dic)
        for line in self.all:
            for i in line.keys():
                if i in priv:
                    new_dic[i]=line[i]

        print(new_dic)

        return new_dic

    def return_pub(self):
        pub=[
            "Population",
            "Culture",
            "Form",
            "Capital",
            "Area"
            ]
        new_dic={}
        for line in self.all:
            for i in line.keys():
                if i in pub:
                    new_dic[i]=line[i]
        return new_dic

    def return_all(self):
        return self.all
    #End of commands
    #################################################################
    #Side funcitonss
    #################################################################
    #Big func
    def bill_army(self):
        self.armies_pay=self.get_armies_pay("Army")
        self.army_pay=self.get_army_pay(self.armies_pay)
        self.navies_pay=self.get_armies_pay("Navy")
        self.navy_pay=self.get_army_pay(self.navies_pay)

    #End of Big func

    #Functions to get single values
    def get_all(self, fname):
        with open("info/"+fname) as file:
            read=csv.reader(file)
            new=[]
            i=0
            name=self.name_capital()
            #print(name)
            for line in read:
                new.append(line)
                #print(line[0])
                if name in line:
                    country=i
                i+=1
        return country, new

    def get_income_class(self, clas, aclas):
        #self.education.literacy=1
        #self.economy["Economy_tier"]="Rural4"
        tier=float(self.tiers[self.economy["Economy_tier"].upper()][clas])
        return tier*float(self.economy["Pop_ratio"][aclas])

    def get_income(self):
        all_income=0
        for income in self.incomes.values():
            all_income+=income
        return all_income

    def get_actual_income(self):
        normal_pay=self.income*float(self.economy["Tax_rate"])/100
        #print(int(normal_pay))
        normal_pay*=int((int(self.economy["Trade"])-1)/20)/5+1
        #print(int(normal_pay))
        #print(normal_pay)
        if self.basics["Stability"]<50:
            normal_pay=normal_pay*float(self.basics["Stability"])/50
            #print(normal_pay)
        normal_pay=int(normal_pay-self.expense)
        print(normal_pay)
        return normal_pay

    def get_armies_pay(self, type):
        armies_pay={}
        #print(self.military_pay)
        #print(self.army_new)
        for unit in self.army_new[type].keys():
            #print(unit)
            unit_stats=self.military_pay[unit]
            stability_pay=float(unit_stats["Maintainance"])*float(unit_stats["Stab_multi"])*(100-float(self.basics["Stability"]))
            armies_pay[unit]=float(unit_stats["Maintainance"])*int(self.army_new[type][unit])+(stability_pay*int(self.army_new[type][unit]))
        return armies_pay

    def get_army_pay(self, dic):
        all_pay=0
        for pay in dic.values():
            all_pay+=pay
        return all_pay

    def get_expenses(self):
        expenses=0
        for expense in self.expenses.values():
            expenses+=float(expense)
        return expenses

    def get_avarage_pay(self):
        pop_ratio=self.economy["Pop_ratio"]
        work_pop=float(pop_ratio["Rpop"])+float(pop_ratio["Ipop"])
        avarage_pay=self.income/work_pop
        #print(avarage_pay)
        return avarage_pay-(avarage_pay*float(self.economy["Tax_rate"])/100)

    def get_avarage_ben(self):
        return float(self.expenses["Benefits_spending"])/float(self.basics["Population"])

    def get_young(self):
        return int(int(self.basics["Population"])*0.3*(float(self.education["Literacy"])/100))

    def get_manpower(self):
        manpower=0
        for key in self.army_new["Army"].keys():
            #print(self.army_new["Army"][key])
            manpower+=int(self.army_new["Army"][key])*float(self.military_pay[key]["Manpower"])
        return manpower

    def get_stab_mod(self, money):
        literacy=1-abs((50-float(self.education["Literacy"]))/50)
        money=(money-20)/200
        #print(literacy)
        if money>0:
            modifier=money*literacy
            modifier=modifier*int(self.stability_tiers[self.basics["Stability_mod"].upper()]["Modifier"])/100
        else:
            try:
                modifier=money/literacy
                modifier=modifier/int(self.stability_tiers[self.basics["Stability_mod"].upper()]["Modifier"])*100
            except ZeroDivisionError:
                modifier=0
        return modifier

    def get_employed(self, rest_pop, clas):
        print(rest_pop)
        #print(self.tiers)
        self.economy["Pop_ratio"][clas]=int(rest_pop*float(self.tiers[self.economy["Economy_tier"].upper()][clas])/100)
        print(self.economy["Pop_ratio"][clas])
        return self.economy["Pop_ratio"][clas]

    def get_estimate(self, upper, lower, num, high, low, mid):
        if float(num)<lower:
            return low
        elif float(num)>upper:
            return high
        else:
            return mid

    def get_round(self, upper, lower, num):
        if float(num)<lower:
            return lower
        elif float(num)>upper:
            return upper
        else:
            return num
    #######################

    def debug_foo(self):
        return self.all

def country_init(name):
    overwrite=[
        "Population",
        "Stability",
        "Stability_mod"
        ]
    eco=[
        "Economy_tier",
        "Tax_rate",
        "Budget",
        "Trade"
        ]
    expenses=[
        "Technology_spending",
        "Benefits_spending",
        "Economy_spending"
        ]
    education=[
        "Literacy",
        "Tech"
        #"ease":0.5,
        #"genious":0.01
        ]
    army={
        "SOL":0,
        "ARCH":0,
        "CAV":0,
        "ART":0,
        "CON":0,
        "LIGH":0,
        "HEAV":0,
        "BORD":0
        }
    pub=[
        "Culture",
        "Form",
        "Capital",
        "Area"
        ]
    manuals={
        "Economy_tier":[str, ["Rural1, Rural2, Rural3, Rural4, Ind1, Ind2, Ind3, Ind4,Mix1, Mix2"]], #change the none value later
        "Stability_mod":[str, [None]], #change the none value later
        "Population":[int, [None]],
        "Area":[float, [None]],
        "Form":[str, [None]],
        "Culture":[str, [None]],
        "Stability":[int, [0, 100]],
        "Literacy":[int, [0, 100]],
        "Army":[int, [None]],
        "Trade":[int, [0, 100]]
        }
    manuals2={
        "Tax_rate":[float, [0, 100]],
        "Technology_spending":[float, [None]],
        "Benefits_spending":[float, [None]],
        "Economy_spending":[float, [None]],
        "Capital":[str, [None]],
        }
    country_now=country(name.upper(), overwrite, eco, expenses, army, education, manuals, manuals2, pub)
    return country_now

if __name__=="__main__":
    #'''
    manuals={
        "Economy_tier":"TIER1",
        "Stability_mod":1
        }
    overwrite={
        "Population":100000,
        "Stability":10,
        "Stability_mod":manuals["Stability_mod"]
        }
    overwrite2=list(overwrite.keys())
    eco={
        "Economy_tier":manuals["Economy_tier"],
        #"Pop_ratio":{"Rural":2, "Artisan":2, "Unemployed":1, "Young":4, "Army":1},
        "Tax_rate":20,
        "Budget":0,
        "Trade":0
        }
    eco2=list(eco.keys())
    expenses={
        "Technology_spending":1000,
        "Benefits_spending":1000,
        "Economy_spending":1000
        }
    expenses2=list(expenses.keys())
    army={
        "SOL":0,
        "ARCH":0,
        "CAV":0,
        "ART":0,
        "CON":0,
        "LIGH":0,
        "HEAV":0,
        "BORD":0
        }
    army2=list(army.keys())
    education={
        "Literacy":20,
        "Tech":0
        #"ease":0.5,
        #"genious":0.01
        }
    education2=list(education.keys())
    manuals={
        "Economy_tier":[str, [None]], #change the none value later
        "Stability_mod":[str, [None]], #change the none value later
        "Population":[int, [None]]
        }
    manuals2={
        "Tax_rate":[float, [0, 100]],
        "Technology_spending":[float, [None]],
        "Building_spending":[float, [None]],
        "Benefits_spending":[float, [None]],
        "Economy_spending":[float, [None]],
        "Army":[str, [None]],
        "Capital":[str, [None]]
        }
    pub=[
        "Culture",
        "Form",
        "Capital",
        "Area"
        ]
    altafia=country("Altafia".upper(), overwrite2, eco2, expenses2, army, education2, manuals, manuals2, pub)
    #altafia.update_stability()
    #altafia.update_income()
    #print(altafia.actual_income)
    #print(altafia.change("Tax_rate", "30"))
    #altafia.return_priv()
    #print(altafia.update_budget())
    #print(altafia.debug_foo())
    print(altafia.update_save())
    #altafia.wierd()
    #input()
    #'''
    #country_init("Altafia")
