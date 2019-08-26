import csv
from pymprog import *


class Drink:

    def __init__(self, name,id):
        self.drink = name
        self.drinkingredientslist = []
        self.id = id

    def __iter__(self):
        return iter(self.list)

    def get_drink(self):
        return self.drink

    def add_drinkingredient(self, name, ingredient):
        self.drinkingredientslist.append(ingredient)
        return self.drinkingredientslist

    def get_drinkingredientslist(self):
        return self.drinkingredientslist

    def get_id(self):
        return self.id

class Ingredient:

    def __init__(self, ingredient,id):
        self.ingredient = ingredient
        self.qte = 0
        self.id = id

    def __iter__(self):
        return iter(self.list)

    def get_ingredient(self):
        return self.ingredient

    def add_qte(self):
        self.qte +=1
        return self.qte

    def get_qte(self):
        return self.qte

    def get_id(self):
        return self.id

class AllIngredients:
    def __init__(self):
        self.ingredients = {}
        self.ingredientslist = []
        self.drinks = {}
        self.drinkslist = []

    def __iter__(self):
        return iter(self.ingredients.values())

    def add_ingredient(self, ingredient,id):
        new_name = Ingredient(ingredient,id)
        self.ingredients[ingredient] = new_name
        self.ingredientslist.append(ingredient)
        return new_name

    def get_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return self.ingredients[ingredient]
        else:
            return None

    def get_ingredientslist(self):
        return self.ingredientslist

    def get_numberedingredient(self, id):
        for ingredient in self.ingredientslist:
            if self.ingredients[ingredient].get_id()==id:
                return self.ingredients[ingredient].get_ingredient()

class AllDrinks:
    def __init__(self):
        self.drinks = {}
        self.drinkslist = []

    def __iter__(self):
        return iter(self.drinks.values())

    def add_drink(self, drink,id):
        new_name = Drink(drink,id)
        self.drinks[drink] = new_name
        self.drinkslist.append(drink)
        return new_name

    def get_drink(self, drink):
        if drink in self.drinks:
            return self.drinks[drink]
        else:
            return None

    def get_drinkslist(self):
        return self.drinkslist

    def get_numbereddrink(self, id):
        for drink in self.drinkslist:
            if self.drinks[drink].get_id()==id:
                return self.drinks[drink].get_drink()

def main():
    pass

def dbdrinks():
    #initialiser la base de donnees
    data_file = "db_drinks.csv"
    with open(data_file) as csvfile:
        f = list(csv.DictReader(csvfile))

    D = AllDrinks()
    I = AllIngredients()
    ingr = "strIngredient"
    alldrinkingredients = []


    i = 1
    while i<=15:
        ingred = ingr+str(i)
        alldrinkingredients.append(ingred)
        i+=1

    d = 1
    for line in f:
        drink = line['strDrink']
        D.add_drink(drink,d)
        d+=1

        for i in alldrinkingredients:
            ingredient = str.lower(line[i])
            if ingredient != "":
                (D.get_drink(drink)).add_drinkingredient((D.get_drink(drink)),ingredient)
                if ingredient not in I.get_ingredientslist():
                    I.add_ingredient(ingredient,(len(I.get_ingredientslist())))

    return D, I

def transformtable(D, I):

    ingredientslist = I.get_ingredientslist()

    laliste=['cocktail']+ingredientslist

    contraintes = []
    nb_ingredients_par_drink = []

    for d in D:
        numlist = []
        for i in ingredientslist:
            drinkyes = 0
            for di in d.get_drinkingredientslist():
                if i==di:
                    drinkyes = 1
            numlist.append(drinkyes)
        contraintes.append(numlist)
        nb_ingredients_par_drink.append(sum(numlist))


    return contraintes,nb_ingredients_par_drink

def solve_problem(D, I, contraintes, nb_ingredients_par_drink):

    A = contraintes
    d = nb_ingredients_par_drink
    nb_drinks = len(nb_ingredients_par_drink)
    nb_ingredients = len(I.get_ingredientslist())
    begin('basic')
    x = var('x', nb_drinks,kind=bool) #drinks
    y = var('y', nb_ingredients,kind=bool) #ingredients
    sum(y) == 5
    maximize(sum(x))

    for i in range(nb_drinks):
      sum(A[i][j]*y[j] for j in range(nb_ingredients))-d[i]*x[i] >= 0
    solve() # resoudre le modele
    print("###>Valeur de la fonction-objectif: %f"%vobj())


    print("variable drinks")
    for i in range(nb_drinks):

        if x[i].primal > 0:
            print(D.get_numbereddrink(i))
            print("x",x[i].primal)
    print("variable ingredients")
    for i in range(nb_ingredients):
        if y[i].primal > 0:
            print(I.get_numberedingredient(i))
            print("y",y[i].primal)

    end()

def optimize_drinks():

    D, I = dbdrinks()
    contraintes, nb_ingredients_par_drink = transformtable(D,I)
    solve_problem(D, I, contraintes, nb_ingredients_par_drink)

if __name__ == '__main__':

    optimize_drinks()
