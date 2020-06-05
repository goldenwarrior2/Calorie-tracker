import json


class Month:
    def __init__(self, lod):
        self.lod = lod


class Day:
    def __init__(self, lom):
        self.lom = lom
        self.listofmealdictionaries = []
        self.month = input('What month is it?' + '\n')
        self.day = int(input('What day of the month is it?' + '\n'))
        self.year = int(input('What year is it?' + '\n'))
        self.total_cal = 0
        self.total_carb = 0
        self.total_protein = 0
        self.total_fat = 0

    def calculate_total(self):
        for i in range(len(self.lom)):
            self.lom[i].calculate_meal_total()
            self.total_cal += self.lom[i].total_cal
            self.total_carb += self.lom[i].total_carb
            self.total_protein += self.lom[i].total_protein
            self.total_fat += self.lom[i].total_fat

    def create_meal_dictionaries(self):
        meal = {}
        for i in self.lom:
            meal['name'] = i.name
            meal['food'] = i.lofstrings
            meal['serving size'] = i.lofservingsize
            meal['servings'] = i.lofservings
            meal['calories'] = i.total_cal
            meal['carbohydrates'] = i.total_carb
            meal['protein'] = i.total_protein
            meal['fat'] = i.total_fat
            self.listofmealdictionaries.append(meal)
            meal = {}
        return self.listofmealdictionaries

    def create_entry(self, month, day, year):
        self.calculate_total()
        new_log = str(month) + '/' + str(day) + '/' + str(year)
        for i in range(len(self.lom)):
            new_log += '\n' + self.lom[i].name + ': ' + str(self.lom[i].list_food_names) + '\n' * 2
            for j in range(len(self.lom[i].lof)):  # loops through the list of foods of all meals of the day
                food = self.lom[i].lof[j]          # individual food of each individual meal
                new_log += ' ' + food.name + ': ' + 'calories ' + str(food.calories) + ', ' + \
                    'protein ' + str(food.protein) + ', ' + \
                    'carbohydrates ' + str(food.carbohydrates) + ', ' + \
                    'fats ' + str(food.fats) + '\n'
            new_log += '\n' + 'Total: ' + 'calories ' + str(self.lom[i].total_cal) + ', carbohydrates ' + \
                       str(self.lom[i].total_carb) + ', protein ' + str(self.lom[i].total_protein) + \
                       ', fat ' + str(self.lom[i].total_fat) + ('\n' * 2)
        new_log += '\n' + 'Total: ' + 'calories ' + str(self.total_cal) + ', carbohydrates ' + \
                   str(self.total_carb) + ', protein ' + str(self.total_protein) + \
                   ', fat ' + str(self.total_fat) + ('\n' * 5)
        print(new_log)
        return new_log

    def entry_to_text(self, txt='tristan macro tracker.txt'):
        with open(txt, 'a') as f:
            f.write(self.create_entry(self.month, self.day, self.year))

    def entry_to_json(self, txt='days tracker.json'):
        send_to_text = input('Would you like to save this day in the text file?\n')
        if send_to_text == 'yes':
            self.entry_to_text()
        else:
            self.create_entry(self.month, self.day, self.year)
            day_entry = {self.month + '/' + str(self.day) + '/' + str(self.year):
                             {'meals': [self.create_meal_dictionaries],
                              'calories': self.total_cal,
                              'carbohydrates': self.total_carb,
                              'protein': self.total_protein,
                              'fat': self.total_fat}
                         }
            with open(txt) as f:
                data = json.load(f)
                data['days'].append(day_entry)
            with open(txt, 'w') as f:
                json.dump(data, f, indent=2)

    # def edit_day(self):


class Meal:
    def __init__(self, name, lof):
        self.name = name
        self.lof = lof                    # lof (list of foods)
        self.lofstrings = []     # lof (strings for the file)
        self.lofservingsize = []
        self.lofservings = []
        self.total_cal = 0
        self.total_carb = 0
        self.total_protein = 0
        self.total_fat = 0
        self.list_food_names = []
        for i in range(len(lof)):
            self.list_food_names.append(str(lof[i].servings) + ' (' + str(lof[i].servingsize) + ') ' + lof[i].name)

    def calculate_meal_total(self):
        for i in range(len(self.lof)):
            self.total_cal += self.lof[i].calories
            self.total_carb += self.lof[i].carbohydrates
            self.total_protein += self.lof[i].protein
            self.total_fat += self.lof[i].fats

    def create_list_of_strings(self):
        for i in self.lof:
            self.lofstrings.append(i.name)
        return self.lofstrings

    def create_list_of_servingsize(self):
        for i in self.lof:
            self.lofservingsize.append(i.servingsize)
        return self.lofservingsize

    def create_list_of_servings(self):
        for i in self.lof:
            self.lofservings.append(i.servings)
        return self.lofservings

    # def edit_meal(self):

    # def store_meal(self):


class Food:
    def __init__(self, name, calories, carbohydrates, protein, fats):
        self.name = name
        self.calories = calories
        self.carbohydrates = carbohydrates
        self.protein = protein
        self.fats = fats
        self.servingsize = 0
        self.servings = 0

    def new_food_entry(self, filename='food macros.json'):
        food_entry = {'name': self.name,
                      'calories': self.calories,
                      'carbohydrates': self.carbohydrates,
                      'protein': self.protein, 'fats': self.fats}
        with open(filename) as f:
            data = json.load(f)
            data['food'].append(food_entry)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def getServingsize(self, servingsize):
        self.servingsize = servingsize
        return self.servingsize

    def actual_serving_size(self, servingsize):
        self.getServingsize(servingsize)
        self.calories *= servingsize
        self.carbohydrates *= servingsize
        self.protein *= servingsize
        self.fats *= servingsize

    def getServings(self, amountservings):
        self.servings = amountservings
        return self.servings

    def amount_of_servings(self, amountservings):
        self.getServings(amountservings)
        self.calories *= amountservings
        self.carbohydrates *= amountservings
        self.protein *= amountservings
        self.fats *= amountservings

    def createServingsize(self):
        servingsize = float(input('What portion of a serving did you have? (must be a float!!)' + '\n'))
        self.actual_serving_size(servingsize)

    def createServings(self):
        amountservings = int(input('How many servings did you have?' + '\n'))
        self.amount_of_servings(amountservings)


def checkFood(food_name, file='food macros.json'):
    with open(file) as f:
        data = json.load(f)
    for food in data['food']:
        if food['name'] == food_name:
            print('food already in file!')
            food = Food(food['name'], food['calories'], food['carbohydrates'], food['protein'], food['fats'])
            food.createServingsize()
            food.createServings()
            return food
    else:
        cal = float(input("How many calories is " + food_name + '?\n'))
        carbs = float(input("How many carbohydrates are in " + food_name + '?\n'))
        protein = float(input("How much protein is in " + food_name + '?\n'))
        fat = float(input("How much fat is in " + food_name + '?\n'))
        new_food = Food(food_name, cal, carbs, protein, fat)
        new_food.new_food_entry(filename='food macros.json')
        new_food.createServingsize()
        new_food.createServings()
        return new_food


def check_input(meal):
    question = input('Did you correctly input all of the information?' + '\n')
    if question == 'no':
        fix_input_values(meal)


def fix_input_values(meal, file='food macros.json'):
    incorrect_food = input('Which food was entered incorrectly?\n')
    for j in range(len(meal.lof) - 1):
        if meal.lof[j].name == incorrect_food:
            meal.lof.remove(meal.lof)
    delete_food = input('Do you want to delete this food from this meal?\n')
    if delete_food == 'yes':
        for i in range(len(meal.lof)):
            if meal.lof[i].name == incorrect_food:
                meal.lof.remove(meal.lof[i])
                meal.lofstrings.remove(meal.lof[i].name)
                meal.lofservingsize.remove(meal.lof[i].servingsize)
                meal.lofservings.remove(meal.lof[i].servings)
    delete_from_file = input('Do you want to delete this food from the food file?\n')
    if delete_from_file == 'yes':
        with open(file) as f:
            data = json.load(f)
        for food in data['food']:
            if food['name'] == incorrect_food:
                data['food'].remove(food)
    answer = input('Is this a new food that you are trying to add to the food dictionary?\n')
    if answer == 'yes':
        with open(file) as f:
            data = json.load(f)
        for food in data['food']:
            if food['name'] == incorrect_food:
                food['name'] = input('Would you like to rename this food? If not, just type in '
                                     + incorrect_food + '\n')
                incorrect_food = food['name']
                food['calories'] = float(input('How many calories are in ' + food['name'] + '?\n'))
                food['carbohydrates'] = float(input('How many carbohydrates are in ' + food['name'] + '?\n'))
                food['protein'] = float(input('How much protein is in ' + food['name'] + '?\n'))
                food['fats'] = float(input('How much fat is in ' + food['name'] + '?\n'))
        with open('food macros.json', 'w') as f:
            new_data = json.dump(data, f, indent=2)
        with open(file) as f:
            data = json.load(f)
        for food in data['food']:
            if food['name'] == incorrect_food:
                food = Food(food['name'], food['calories'], food['carbohydrates'], food['protein'], food['fats'])
                meal.lof.append(food)
                servingsize = float(input('What portion of a serving did you have? (must be a float!!)\n'))
                food.actual_serving_size(servingsize)
                amountservings = float(input('How many servings did you have?\n'))
                food.amount_of_servings(amountservings)
    else:
        for i in range(len(meal.lof)):
            if meal.lof[i].name == incorrect_food:
                meal.lof[i].servingsize = float(input('What portion of a serving did you have? (must be a float!!)\n'))
                meal.lof[i].actual_serving_size(meal.lof[i].servingsize)
                meal.lof[i].servings = int(input('How many servings did you have?\n'))
                meal.lof[i].amount_of_servings(meal.lof[i].servings)


def create_meal(food_list):
    new_food = input('Please add a food to this meal.\n')
    while new_food != 'no':
        food_list.append(checkFood(new_food))
        new_food = input('Is there any more food that you would like to add?\n')
    return food_list


def entry_for_today(file='days tracker.json'):
    question = input('Would you like to add a new day or add to an existing one?\n')
    if question == 'new day':
        create_day()
    # else:
    #     date = input('Which day would you like to add to?')
    #     with open(file) as f:
    #         data = json.load(f)
    #     for day in data['days']:
    #         if day['name'] == date:
def create_day():
    list_of_foods = []
    list_of_meals = []
    meal_name = input('Please add your first meal.\n')
    while meal_name != 'no':
        new_food_list = create_meal(list_of_foods)
        new_meal = Meal(meal_name, new_food_list)
        new_meal.create_list_of_strings()
        new_meal.create_list_of_servings()
        new_meal.create_list_of_servingsize()
        check_input(new_meal)
        list_of_meals.append(new_meal)
        list_of_foods = []
        meal_name = input('Would you like to add another meal?\n')
    today = Day(list_of_meals)
    today.entry_to_json()


entry_for_today()



