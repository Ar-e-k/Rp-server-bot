import csv
from copy import copy

class country:

    def __init__(self, name, overwrite, economy, expenses, army, education, manuals, manuals2, public):
        self.admin_manuals=manuals
        self.user_manuals=manuals2
        self.admin_manuals.update(self.user_manuals)
        all=self.read_stats("World_priv.csv")
        self.name=name
        #print(all)
        #print()
        #print(economy)
        #print(self.name)
        #print(all)
        #print(all[self.name])
        #self.all=all[self.name]
        '''print(self.all)
        print(self.all[self.name])
        print(self.name)
        print("_______________________________________________________________________________\n\n\n\n")'''
        all=all[self.name]
        #print(all)
        #'''
        self.basics={}
        self.create_dic(self.basics, overwrite, all)
        self.economy={}
        self.economy["Pop_ratio"]={"Rural":0, "Industrial":0, "Unemployed":0, "Young":0, "Army":0}
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
        #print("helo")
        #print(army_new)
        for unit in range(0, 4):
            #print(self.army_new["Army"][unit])
            army_new[unit]=army_new[unit][2:-1]
        #print(army_new)
        self.army_new={"Army":dict(zip(["SOL", "ARCH", "CAV", "ART"], army_new))}
        #print(self.army_new["Army"])
        #print(self.economy)
        self.all=[self.basics, self.economy, self.expenses, self.education, self.public, self.army_new]

        '''
        self.army={}
        self.create_dic(self.army, army, all)
        self.basics=overwrite
        self.economy=economy
        self.Tier=self.economy["Tier"]
        self.Pop_ratio=self.economy["Pop_ratio"]
        self.Tax_rate=self.economy["Tax_rate"]
        self.expenses=expenses
        #'''
        self.army=army

    def wierd(self):
        all=self.read_stats("World_priv.csv")
        all=all[self.name]
        print(self.all)
        '''print("\n\n\n")
        print(all)
        print("\n\n\n")
        print(list(self.admin_manuals.keys()))
        print("\n\n\n")
        print(type(all))'''
        for i in list(self.admin_manuals.keys()):
            #print(all[i])
            all.pop(i)
        print("\n\n\n")
        #print(all)
        for cat in self.all:
            for key in cat.keys():
                if key in all:
                    self.all[self.all.index(cat)][key]=all[key]
                else:
                    pass
        print(self.all)

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
            #print(head)
            if head=="Army":
                #print(new_dic[head])
                new_list.append(list(new_dic[head].values()))
                continue
            new_list.append(new_dic[head])
        new_list.insert(0, name)
        new[country]=new_list
        self.write_stats(fname, new)

    def edit_stats_value(self, fname, value, source):
        country, new=self.get_all(fname)
        #print(new[0].index(country))
        source=new[0].index(source)
        #print(source)
        #print(new[country])
        new[country][source]=value
        self.write_stats(fname, new)

    def name_capital(self):
        name=self.name.lower()
        name=list(name)
        name[0]=name[0].upper()
        if " " in name:
            for pos in range(0, len(name)-1):
                try:
                    #print(name[pos]==" ", name[pos+1]!="o")
                    if name[pos]==" " and name[pos+1]!="o":
                        #print("here", name[name.index(letter)+1])
                        name[pos+1]=name[pos+1].upper()
                    else:
                        pass
                except IndexError:
                    pass
        name="".join(name)
        return name

    def edit_name(self, fname, value):
        country, new=self.get_all(fname)
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
        #print(self.all)
        error=self.update_budget()
        if error==None:
            pass
        else:
            return error
        self.edit_stats("World_priv.csv")
        return None

    def update_budget(self): #Updates the overall country budget
        self.update_income()
        #print(self.economy)
        self.economy["Budget"]=float(self.economy["Budget"])+self.actual_income
        return self.check_budget()

    def check_budget(self):
        print(self.income, self.actual_income+self.expense)
        if self.economy["Budget"]<=0:
            print(self.economy["Budget"])
            if self.actual_income<0:
                print("You fucked up", self.actual_income)
                det=self.economy["Budget"]
                last_bug=float(self.economy["Budget"])-self.actual_income
                over=self.actual_income+self.expense-det
                print(last_bug, det)
                print(over, self.expense)
                self.wierd()
                text=self.name+" is out of budget, please contact them to limit spendings or get a loan"
                return text
            else:
                print("interesting (its a bug)")

    def update_income(self): #Updates the actual income of the country
        self.update_stability()
        self.update_expenses()
        #sefl.update_per_income()
        self.actual_income=self.get_actual_income()

    def update_per_income(self): #Updates income per Rural and Industrial population
        try:
            1 in self.tiers
        except AttributeError:
            self.tiers=self.read_stats("economy.csv")
        self.update_ratio()
        self.incomes={}
        self.incomes["Rural"]=self.get_income_class("Rural")
        self.incomes["Industrial"]=self.get_income_class("Industrial")

    def update_expenses(self): #Updates country spendings
        self.expense=0
        self.bill_army()
        self.expenses["army"]=self.army_pay
        self.expense+=self.get_expenses()

    def update_stability(self): #Updates stablility
        self.update_literacy()
        modifier=0
        literacy=1-abs((50-float(self.education["Literacy"]))/50)
        self.update_per_income()
        self.income=self.get_income()
        avarage_pay=self.get_avarage_pay()
        avarage_ben=self.get_avarage_ben()
        self.basics["Stability"]=50
        #print(literacy)
        #print(avarage_pay/100)
        #print(avarage_ben)
        modifier=literacy+avarage_pay/100
        self.basics["Stability"]+=modifier
        if self.basics["Stability"]>100:
            self.basics["Stability"]=100
        elif self.basics["Stability"]<0:
            self.basics["Stability"]=0
        else:
            pass

    def update_literacy(self): #Updates literacy, the amount of people in the country that are able to read&write
        spending=float(self.expenses["Technology_spending"])/float(self.basics["Population"])
        change=-(1-spending)
        #print(self.education["Literacy"])
        #print(spending)
        #print(change)
        #print(change/float(self.education["Literacy"]))
        self.education["Literacy"]=change+float(self.education["Literacy"])
        if self.education["Literacy"]>100:
            self.education["Literacy"]=100
        elif self.education["Literacy"]<0:
            self.education["Literacy"]=0
        else:
            pass

    def update_ratio(self): #Updates the amount of each group of people in the society
        self.economy["Pop_ratio"]["Young"]=self.get_young()
        try:
            1 in self.military_pay
        except AttributeError:
            self.military_pay=self.read_stats('army_expences.csv')
        self.economy["Pop_ratio"]["Army"]=self.get_manpower()
        rest_pop=float(self.basics["Population"])-(self.economy["Pop_ratio"]["Army"]+self.economy["Pop_ratio"]["Young"])
        employment=0
        #print(rest_pop)
        for clas in ["Rural", "Industrial"]:
            employment+=self.get_employed(rest_pop, clas)
        unemployed=rest_pop-employment
        self.economy["Pop_ratio"]["Unemployed"]=unemployed
    #End of updating stuff

    #Commands
    def change_name(self, value):
        value=self.edit_name("World_priv.csv", value)
        task="Task successfull\nYour new name is "+self.name
        return task

    def change(self, source, value, admin=False):
        #print(source, value)
        if admin==True:
            manuals=self.admin_manuals
        else:
            manuals=self.user_manuals
        #print(source, value)
        #print(self.user_manuals)
        if source in manuals.keys():
            pass
        else:
            return "Invalid source"
        try:
            value=float(value)
        except ValueError:
            pass
        #print("hello there")
        #print(value, type(value))
        #print(value)
        #print(type(value))
        #print(manuals[source][0])
        if type(value)==manuals[source][0]:
            if None in manuals[source][1]:
                pass
            else:
                if type(value)==str:
                    if value in manuals[source][1]:
                        pass
                    else:
                        return "Invalid value1"
                elif type(value)==float:
                    #print(manuals[source][1])
                    #print(value)
                    #print(manuals[source][1][0], manuals[source][1][1])
                    if value>manuals[source][1][0] and value<manuals[source][1][1]:
                        pass
                    else:
                        return "Invalid value2"
                else:
                    return "Something went wrong"
        else:
            return "Invalid value"
        #try:
        if source in self.economy.keys():
            self.economy[source]=value
        elif source in self.basics.keys():
            self.basics[source]=value
        elif source in self.expenses.keys():
            self.expenses[source]=value
        self.edit_stats_value("World_priv.csv", value, source)
        return "Task sucessfull"

    def return_priv(self):
        priv=[
            "Budget",
            "Population",
            "Tax_rate",
            "Technology_spending",
            "Building_spending",
            "Benefits_spending",
            "Economy_spending",
            "Army"
            ]
        if float(self.basics["Stability"])<35:
            level="Low"
        elif float(self.basics["Stability"])>65:
            level="High"
        else:
            level="Medium"
        new_dic={"Stability":level}
        if float(self.education["Literacy"])<35:
            level="Low"
        elif float(self.education["Literacy"])>65:
            level="High"
        else:
            level="Medium"
        new_dic["Literacy"]=level
        #print(self.all)
        #print(priv)
        for line in self.all:
            for i in line.keys():
                #print(i)
                if i in priv:
                    #print(True)
                    new_dic[i]=line[i]
        #print(new_dic)
        return new_dic

    def return_pub(self):
        pub=[
            "Population",
            "Culture",
            "Form",
            "Capital",
            "Area"
            ]
        #print(self.all)
        new_dic={}
        for line in self.all:
            #print(line)
            for i in line.keys():
                if i in pub:
                    new_dic[i]=line[i]
        return new_dic
    #End of commands
    #################################################################
    #Side funcitons
    #################################################################
    #Big func
    def bill_army(self):
        try:
            1 in self.military_pay
        except AttributeError:
            self.military_pay=self.read_stats('army_expences.csv')
        self.get_armies_pay()
        self.army_pay=self.get_army_pay()
    #End of Big func

    #Functions to get single values
    def get_all(self, fname):
        with open("info/"+fname) as file:
            read=csv.reader(file)
            new=[]
            i=0
            name=self.name_capital()
            for line in read:
                new.append(line)
                if name in line:
                    country=i
                i+=1
        return country, new

    def get_income_class(self, clas):
        tier=float(self.tiers[self.economy["Economy_tier"].upper()][clas])
        #pop_ratio=float(self.economy["Pop_ratio"][clas])
        #print(tier)
        #print(self.basics["Population"])
        return tier*float(self.economy["Pop_ratio"][clas])

    def get_income(self):
        all_income=0
        for income in self.incomes.values():
            all_income+=income
        return all_income

    def get_actual_income(self):
        normal_pay=self.income*float(self.economy["Tax_rate"])/100
        #print(normal_pay)
        return normal_pay*float(self.basics["Stability"])/100-self.expense

    def get_armies_pay(self):
        self.armies_pay={}
        #print(self.military_pay)
        #print("army")
        #print(self.army)
        #print(self.army_new)
        print(self.basics["Stability"])
        for unit in self.military_pay.keys():
            unit_stats=self.military_pay[unit]
            stability_pay=float(unit_stats["Maintainance"])*float(unit_stats["Stab_multi"])*(100-float(self.basics["Stability"]))/2
            self.armies_pay[unit]=float(unit_stats["Maintainance"])*int(self.army_new["Army"][unit])+(stability_pay*int(self.army_new["Army"][unit]))

    def get_army_pay(self):
        all_pay=0
        for pay in self.armies_pay.values():
            all_pay+=pay
        return all_pay

    def get_expenses(self):
        expenses=0
        for expense in self.expenses.values():
            expenses+=float(expense)
        return expenses

    def get_avarage_pay(self):
        pop_ratio=self.economy["Pop_ratio"]
        #print(self.economy["Pop_ratio"])
        indust=float(pop_ratio["Industrial"])
        rural=float(pop_ratio["Rural"])
        work_pop=indust+rural
        #print(self.income)
        #print(work_pop)
        avarage_pay=self.income/work_pop
        return avarage_pay-(avarage_pay*float(self.economy["Tax_rate"])/100)

    def get_avarage_ben(self):
        return float(self.expenses["Benefits_spending"])/float(self.basics["Population"])

    def get_young(self):
        return float(self.basics["Population"])*0.3*(float(self.education["Literacy"])/100)

    def get_manpower(self):
        manpower=0
        for key in self.army_new["Army"].keys():
            manpower+=int(self.army_new["Army"][key])*float(self.military_pay[key]["Manpower"])
        return manpower

    def get_employed(self, rest_pop, clas):
        self.economy["Pop_ratio"][clas]=rest_pop*float(self.tiers[self.economy["Economy_tier"].upper()][clas])/100
        return self.economy["Pop_ratio"][clas]
    #######################

    def debug_foo(self):
        pass

def country_init(name):
    overwrite=[
        "Population",
        "Stability",
        "Stability_mod"
        ]
    eco=[
        "Economy_tier",
        "Tax_rate",
        "Budget"
        ]
    expenses=[
        "Technology_spending",
        "Building_spending",
        "Benefits_spending",
        "Economy_spending"
        ]
    education=[
        "Literacy"
        #"ease":0.5,
        #"genious":0.01
        ]
    army={
        "SOL":0,
        "ARCH":0,
        "CAV":0,
        "ART":0
        }
    pub=[
        "Culture",
        "Form",
        "Capital",
        "Area"
        ]
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
        "Army":[str, [None]]
        }
    country_now=country(name.upper(), overwrite, eco, expenses, army, education, manuals, manuals2, pub)
    return country_now

if __name__=="__main__":
    #country_init("Altafia")
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
        #"Pop_ratio":{"Rural":2, "Industrial":2, "Unemployed":1, "Young":4, "Army":1},
        "Tax_rate":20,
        "Budget":0
        }
    eco2=list(eco.keys())
    expenses={
        "Technology_spending":1000,
        "Building_spending":1000,
        "Benefits_spending":1000,
        "Economy_spending":1000
        }
    expenses2=list(expenses.keys())
    army={
        "SOL":0,
        "ARCH":0,
        "CAV":0,
        "ART":0
        }
    army2=list(army.keys())
    education={
        "Literacy":20#,
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
        "Army":[str, [None]]
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
    print(altafia.update_save())
    #altafia.update_budget()
    #altafia.wierd()
