import csv
from itertools import chain
import random
from datetime import date, timedelta
import unidecode

# Ścieżki do plików CSV
men_name_csv_filepath = './men_name.csv'
women_name_csv_filepath = './women_name.csv'
men_surname_csv_filepath = './men_surname.csv'
women_surname_csv_filepath = './women_surname.csv'

# Funkcje pomocnicze
def read_csv(filepath, surname=False):
    people_quantity = {}
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            name = row[0]
            if surname:
                number = int(row[1])
                people_quantity[name] = {"occurances": number}
            else:
                number = int(row[2])
                gender = row[1]
                people_quantity[name] = {
                    "occurances": number,
                    "gender": gender
                }
    return people_quantity

def merge_two_csv(filepathMen, filepathWoman, surname=False):
    men_data = read_csv(filepathMen, surname)
    woman_data = read_csv(filepathWoman, surname)
    merged_data = {}
    for name, data in men_data.items():
        key = f"{name}_M"
        merged_data[key] = {
            "occurances": data["occurances"],
            "gender": "M"
        }
    for name, data in woman_data.items():
        key = f"{name}_K"
        merged_data[key] = {
            "occurances": data["occurances"],
            "gender": "K"
        }
    return merged_data

def calculate_weights(people_quantity, surname=False):
    total_occurrences = sum(person["occurances"] for person in people_quantity.values())
    weights = {}
    for name, person in people_quantity.items():
        weights[name] = {
            "weight": person["occurances"] / total_occurrences,
        }
        if not surname:
            weights[name]["gender"] = person["gender"]
    return weights

def process_weights_data(filePath1, filePath2, surname=False):
    try:
        people_quantity = merge_two_csv(filePath1, filePath2, surname)
        weight_of_name = calculate_weights(people_quantity)
        return weight_of_name
    except (FileNotFoundError, NameError, ValueError) as e:
        print(f'Error: {e}')

def divideListBasedOnGender(list):
    menList = []
    womanList = []              
    for item in list:
        if item.split("_")[1] == "K":
            womanList.append(item.split("_")[0])
        else:
            menList.append(item.split("_")[0])
    return {"men": menList, "women": womanList}

def calculate_surname_weights(filePath1):
    try:
        surnames = read_csv(filePath1, surname=True)
        weight_of_name = calculate_weights(surnames, surname=True)
        return weight_of_name
    except (FileNotFoundError, NameError, ValueError) as e:
        print(f'Error: {e}')

def get_random_from_list(people, number):
    return random.choices(
        population=list(people.keys()),
        weights=[info["weight"] for info in people.values()],
        k=number
    )

def combie_names_and_surnames(names, surnames):
    return [f"{name} {surname}" for name, surname in zip(names, surnames)]

def generate_pesel_and_phone(dob, gender, phone_pool, contact_phone_pool):
    year, month, day = dob.year, dob.month, dob.day
    if year >= 2000:
        month += 20
    pesel = f"{str(year)[-2:]}{month:02d}{day:02d}"
    random_part = random.randint(0, 999)
    gender_digit = random.choice([0, 2, 4, 6, 8]) if gender == "K" else random.choice([1, 3, 5, 7, 9])
    pesel += f"{random_part:03d}{gender_digit}"
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    control_sum = sum(int(pesel[i]) * weights[i] for i in range(10))
    control_digit = (10 - (control_sum % 10)) % 10
    pesel += str(control_digit)
    
    telefon = phone_pool.pop() if phone_pool else None
    telefon_kontaktowy = contact_phone_pool.pop() if contact_phone_pool and random.random() < 0.9 else None
    return pesel, telefon, telefon_kontaktowy

def generate_people(names, surnames, gender, phone_pool, contact_phone_pool):
    people = []
    for name, surname in zip(names, surnames):
        dob = date.today() - timedelta(days=random.randint(18*365, 100*365))
        pesel, telefon, telefon_kontaktowy = generate_pesel_and_phone(dob, gender, phone_pool, contact_phone_pool)
        
        # Generowanie adresu e-mail
        email_name = unidecode.unidecode(name.lower().replace(" ", ""))
        email_surname = unidecode.unidecode(surname.lower().replace(" ", ""))
        email = f"{email_name}.{email_surname}@wombat.com"
        
        people.append({
            "name": f"{name} {surname}",
            "pesel": pesel,
            "telefon": telefon,
            "telefon_kontaktowy": telefon_kontaktowy,
            "email": email
        })
    return people

# Generowanie unikalnych numerów telefonów
def generate_phone_pool(size):
    phones = [f"48{random.randint(500, 899)}{random.randint(100000, 999999)}" for _ in range(size * 3)]
    return list(set(phones))[:size]  # Zapewniamy unikalność

# Nowe funkcje z pełnymi danymi
def get_names_list(count, men_names, women_names, men_surnames, women_surnames, phone_pool, contact_phone_pool):
    men_count = count // 2
    women_count = count - men_count

    random_men_names = men_names[:men_count]
    random_women_names = women_names[:women_count]
    random_men_surnames = men_surnames[:men_count]
    random_women_surnames = women_surnames[:women_count]

    men = generate_people(random_men_names, random_men_surnames, "M", phone_pool, contact_phone_pool)
    women = generate_people(random_women_names, random_women_surnames, "K", phone_pool, contact_phone_pool)

    return sorted(men + women, key=lambda x: x["name"])

def get_names_list2(count, men_names, women_names, men_surnames, women_surnames, phone_pool, contact_phone_pool):
    men_count = count // 2
    women_count = count - men_count

    random_men_names = men_names[:men_count]
    random_women_names = women_names[:women_count]
    random_men_surnames = men_surnames[:men_count]
    random_women_surnames = women_surnames[:women_count]

    men = generate_people(random_men_names, random_men_surnames, "M", phone_pool, contact_phone_pool)
    women = generate_people(random_women_names, random_women_surnames, "K", phone_pool, contact_phone_pool)

    return sorted(men + women, key=lambda x: x["name"])

# Główna logika
people = process_weights_data(men_name_csv_filepath, women_name_csv_filepath)
random_persons = get_random_from_list(people, 500)
dividedList = divideListBasedOnGender(random_persons)
random_men_names_list = dividedList["men"]
random_women_names_list = dividedList["women"]

men_surname_weight_data = calculate_surname_weights(men_surname_csv_filepath)
women_surname_weight_data = calculate_surname_weights(women_surname_csv_filepath)

random_men_surnames = get_random_from_list(men_surname_weight_data, len(random_men_names_list))
random_women_surnames = get_random_from_list(women_surname_weight_data, len(random_women_names_list))

phone_pool = generate_phone_pool(1000)
contact_phone_pool = generate_phone_pool(1000)

names_list1 = get_names_list(
    (500), 
    random_men_names_list, 
    random_women_names_list, 
    random_men_surnames, 
    random_women_surnames, 
    phone_pool, 
    contact_phone_pool
)

names_list2 = get_names_list2(
    6, 
    random_men_names_list, 
    random_women_names_list, 
    random_men_surnames, 
    random_women_surnames, 
    phone_pool, 
    contact_phone_pool
)

def get_names_list3():
   return names_list1
def get_names_list4():
   return names_list2