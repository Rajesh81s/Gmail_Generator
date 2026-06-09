"""
Personal Assistant Bot — Name / Email / Password Generator
Generates realistic names from multiple countries — 90% international / 10% Indian.
70% male, 30% female. DOB always 21–40 years old.

Completely database-free.
"""

import random
import string
from datetime import datetime

# ==================== NAME DATABASE — SEPARATED POOLS ====================

INDIAN_MALE_FIRST = [
    "Aarav", "Aditya", "Akash", "Aman", "Amit", "Anand", "Anil", "Arjun", "Ashish", "Ashok",
    "Bharat", "Chandan", "Chirag", "Deepak", "Devesh", "Dhruv", "Dinesh", "Gaurav", "Harsh", "Hemant",
    "Hitesh", "Ishaan", "Jatin", "Jayesh", "Karan", "Kartik", "Kunal", "Lalit", "Lokesh", "Manish",
    "Mayank", "Mohit", "Mukesh", "Naman", "Naveen", "Nikhil", "Nitin", "Omkar", "Pankaj", "Pawan",
    "Pradeep", "Pranav", "Pratik", "Rahul", "Rajesh", "Rakesh", "Ravi", "Ritik", "Rohan", "Rohit",
    "Sachin", "Sahil", "Sanjay", "Saurabh", "Shivam", "Shubham", "Sumit", "Sunil", "Suresh", "Tushar",
    "Varun", "Vijay", "Vikram", "Vinay", "Vishal", "Vivek", "Yash", "Abhishek", "Ajay", "Alok",
    "Ankur", "Anuj", "Brijesh", "Daksh", "Darshan", "Girish", "Gopal", "Hardik", "Harish", "Himanshu",
    "Kamal", "Kapil", "Krishna", "Madhav", "Manoj", "Neeraj", "Paras", "Piyush", "Raghav", "Rajat",
    "Ramesh", "Rupesh", "Sagar", "Sandeep", "Shreyas", "Siddharth", "Tarun", "Uday", "Utkarsh", "Yogesh",
    "Arnav", "Reyansh", "Vihaan", "Kabir", "Advait", "Rudra", "Atharv", "Tanmay", "Tejas", "Laksh",
    "Ayaan", "Dhairya", "Ishan", "Krish", "Parth", "Samar", "Ved", "Yuvraj", "Aarush", "Ankit",
    "Bhavesh", "Chiranjeev", "Dilip", "Farhan", "Ganesh", "Hari", "Jayant", "Kishore", "Mohan", "Prasad",
    "Nirav", "Rajan", "Sameer", "Sudhir", "Trilok", "Umang", "Venkat", "Yatin", "Zubin", "Sohail",
    "Irfan", "Zeeshan", "Fahad", "Imran", "Arif", "Rizwan", "Tanveer", "Faisal", "Nadeem", "Salman",
    "Vipin", "Bhushan", "Chandresh", "Dheeraj", "Eknath", "Govind", "Hansraj", "Jagdish", "Keshav", "Laxman",
    "Mithun", "Nagesh", "Onkar", "Pramod", "Rajeev", "Satish", "Taran", "Udayan", "Vimal", "Wasim",
    "Yashwant", "Balraj", "Chetan", "Deepesh", "Gagan", "Harjot", "Inderjit", "Jaspal", "Kuldeep", "Lovish",
    "Manpreet", "Narayan", "Omprakash", "Prashant", "Ranbir", "Surinder", "Tejpal", "Vikrant", "Ashwin", "Bhavin",
    "Darshit", "Gaurang", "Hiren", "Jigar", "Keyur", "Mitesh", "Nishant", "Paresh", "Ruchit", "Sanjeet",
]

INDIAN_FEMALE_FIRST = [
    "Aanya", "Aditi", "Aisha", "Ananya", "Anjali", "Anita", "Ankita", "Aparna", "Archana", "Bhavna",
    "Chitra", "Deepa", "Diya", "Divya", "Esha", "Garima", "Hema", "Isha", "Jaya", "Jyoti",
    "Kajal", "Kavita", "Kavya", "Kiran", "Komal", "Lakshmi", "Lata", "Madhu", "Mansi", "Maya",
    "Meena", "Megha", "Nandini", "Neha", "Nidhi", "Nikita", "Nisha", "Pallavi", "Payal", "Pooja",
    "Prachi", "Pragya", "Preeti", "Prisha", "Priya", "Radha", "Ragini", "Rani", "Rashmi", "Rekha",
    "Riya", "Roshni", "Sakshi", "Sandhya", "Sara", "Seema", "Shikha", "Shivani", "Shreya", "Simran",
    "Sneha", "Sonali", "Sonia", "Swati", "Tanvi", "Tara", "Trisha", "Vaishali", "Vandana", "Varsha",
    "Aarohi", "Kiara", "Myra", "Saanvi", "Aadya", "Ira", "Navya", "Pihu", "Siya", "Avni",
    "Bhoomika", "Charvi", "Damini", "Falguni", "Gauri", "Harini", "Janvi", "Kriti", "Latika", "Mitali",
    "Naina", "Parul", "Ritika", "Shalini", "Tanuja", "Urvi", "Vrinda", "Yamini", "Zara", "Anvi",
    "Aanchal", "Barkha", "Chhavi", "Devika", "Ekta", "Geeta", "Heena", "Indu", "Juhi", "Kamini",
    "Laxmi", "Mala", "Namrata", "Prerna", "Rachna", "Sapna", "Teena", "Uma", "Vidya", "Wafaa",
    "Yasmin", "Zeenat", "Amrita", "Bindiya", "Champa", "Dulari", "Guddi", "Hansa", "Jhanvi", "Kanak",
    "Madhuri", "Nirmal", "Padma", "Renu", "Shobha", "Tulsi", "Usha", "Veena", "Yashi", "Alka",
    "Bhagwati", "Chameli", "Durga", "Girija", "Himani", "Jigna", "Kusum", "Manju", "Nirmala", "Pushpa",
]

INDIAN_LAST = [
    "Agarwal", "Arora", "Bansal", "Bhatia", "Bhatt", "Bisht", "Chauhan", "Chopra", "Choudhary", "Das",
    "Desai", "Dubey", "Garg", "Ghosh", "Goyal", "Gupta", "Iyer", "Jain", "Jha", "Joshi",
    "Kapoor", "Kaur", "Khan", "Kohli", "Kumar", "Lal", "Mahajan", "Malhotra", "Mehra", "Mehta",
    "Mishra", "Mittal", "Mukherjee", "Nair", "Negi", "Pandit", "Pandey", "Patel", "Patil", "Prasad",
    "Rai", "Rajput", "Rana", "Rao", "Rathore", "Rawat", "Roy", "Saini", "Saxena", "Sen",
    "Shah", "Sharma", "Shukla", "Singh", "Sinha", "Srivastava", "Thakur", "Tiwari", "Trivedi", "Varma",
    "Verma", "Yadav", "Acharya", "Bajaj", "Bedi", "Bhargava", "Chawla", "Deshpande", "Dutta", "Gill",
    "Grewal", "Hegde", "Khatri", "Kulkarni", "Rastogi", "Reddy", "Sethi", "Tandon", "Walia", "Oberoi",
    "Dhawan", "Bajpai", "Chandra", "Dewan", "Grover", "Kaushik", "Khanna", "Mathur", "Narayan", "Naik",
    "Pillai", "Sachdev", "Sahni", "Sodhi", "Suri", "Vohra", "Wadhwa", "Rajan", "Hora", "Sagar",
    "Ahuja", "Bakshi", "Bhalla", "Chugh", "Dang", "Goel", "Gulati", "Juneja", "Kalra", "Luthra",
    "Madan", "Nagpal", "Puri", "Sabharwal", "Talwar", "Uppal", "Vashisht", "Wahi", "Anand", "Batra",
    "Chadha", "Dhingra", "Gujral", "Handa", "Jaggi", "Kakkar", "Manchanda", "Narula", "Pahwa", "Sachdeva",
    "Trehan", "Behl", "Chhabra", "Duggal", "Kapahi", "Monga", "Pasricha", "Rekhi", "Sehgal", "Waraich",
    "Bhasin", "Chaudhuri", "Deol", "Ghai", "Johar", "Kochhar", "Mannan", "Randhawa", "Sandhu", "Sidhu",
]

US_MALE_FIRST = [
    "James", "John", "Robert", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Charles",
    "Daniel", "Matthew", "Anthony", "Mark", "Steven", "Paul", "Andrew", "Joshua", "Kevin", "Brian",
    "Ryan", "Jason", "Brandon", "Justin", "Tyler", "Austin", "Nathan", "Aaron", "Jacob", "Ethan",
    "Mason", "Logan", "Lucas", "Liam", "Noah", "Oliver", "Aiden", "Elijah", "Jackson", "Carter",
    "Dylan", "Luke", "Gabriel", "Owen", "Caleb", "Connor", "Isaac", "Jayden", "Hunter", "Adrian",
    "Evan", "Ian", "Marcus", "Cole", "Derek", "Troy", "Scott", "Kyle", "Blake", "Chase",
    "Gavin", "Trevor", "Spencer", "Carl", "Alex", "Max", "Leo", "Nolan", "Miles", "Grant",
    "Dean", "Eric", "Sean", "Patrick", "Victor", "Ray", "Craig", "Keith", "Roger", "Frank",
    "Brett", "Brent", "Cody", "Dustin", "Eddie", "Felix", "Greg", "Henry", "Ivan", "Jack",
    "Kent", "Larry", "Mike", "Neil", "Oscar", "Pete", "Quinn", "Ross", "Steve", "Todd",
    "Vince", "Wade", "Xavier", "Zach", "Cameron", "Wesley", "Brody", "Carson", "Cooper", "Hudson",
    "Wyatt", "Colton", "Tanner", "Dalton", "Landon", "Travis", "Mitchell", "Kendrick", "Donovan", "Riley",
    "Ashton", "Bennett", "Calvin", "Dominic", "Emerson", "Finn", "Greyson", "Holden", "Isaiah", "Jace",
    "Kai", "Lawrence", "Maddox", "Nathaniel", "Orlando", "Preston", "Remington", "Silas", "Tristan", "Uriel",
    "Vincent", "Walter", "Xander", "Yusuf", "Zander", "Abel", "Brooks", "Clayton", "Damon", "Elliott",
    "Floyd", "Graham", "Hector", "Jared", "Kenneth", "Lincoln", "Marshall", "Newton", "Omar", "Porter",
    "Quincy", "Reese", "Sullivan", "Terrence", "Ulysses", "Vernon", "Winston", "Alvin", "Bernard", "Clifford",
    "Dennis", "Edgar", "Frederick", "Gerald", "Harold", "Jerome", "Kirk", "Leonard", "Morris", "Norman",
    "Percy", "Randall", "Sherman", "Theodore", "Warren", "Albert", "Bruce", "Cedric", "Darren", "Ernest",
    "Franklin", "Gilbert", "Harvey", "Irving", "Julius", "Karl", "Lewis", "Melvin", "Nelson", "Russell",
]

US_FEMALE_FIRST = [
    "Emily", "Sarah", "Jessica", "Ashley", "Amanda", "Jennifer", "Lauren", "Megan", "Samantha", "Rachel",
    "Nicole", "Hannah", "Brittany", "Kayla", "Olivia", "Emma", "Sophia", "Ava", "Isabella", "Mia",
    "Chloe", "Grace", "Lily", "Ella", "Zoe", "Madison", "Abigail", "Natalie", "Victoria", "Hazel",
    "Riley", "Nora", "Stella", "Lucy", "Aria", "Scarlett", "Claire", "Leah", "Brooke", "Morgan",
    "Taylor", "Tiffany", "Amber", "Crystal", "Heather", "Kelly", "Vanessa", "Courtney", "Dana", "Paige",
    "Audrey", "Bella", "Caroline", "Daisy", "Elena", "Faith", "Gabriella", "Harper", "Iris", "Julia",
    "Katherine", "Laura", "Mackenzie", "Naomi", "Peyton", "Reagan", "Sierra", "Trinity", "Violet", "Wendy",
    "Alexis", "Bethany", "Chelsea", "Diana", "Evelyn", "Fiona", "Giselle", "Holly", "Ivy", "Jasmine",
    "Kendra", "Lindsey", "Marissa", "Nina", "Ophelia", "Penelope", "Quinn", "Rebecca", "Shelby", "Tessa",
    "Una", "Valerie", "Whitney", "Ximena", "Yolanda", "Zelda", "Addison", "Brianna", "Carmen", "Destiny",
    "Elise", "Francesca", "Gloria", "Harmony", "Imogen", "Josephine", "Kaitlyn", "Lydia", "Miranda", "Noelle",
    "Olive", "Priscilla", "Rosemary", "Sadie", "Tabitha", "Ursula", "Vera", "Willa", "Annabelle", "Beatrice",
    "Celeste", "Dorothy", "Estelle", "Florence", "Genevieve", "Harriet", "Ingrid", "Jacqueline", "Kathleen", "Louise",
]

US_LAST = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Wilson", "Anderson", "Taylor", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Moore",
    "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Green",
    "Baker", "Adams", "Nelson", "Hill", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans",
    "Turner", "Parker", "Collins", "Edwards", "Stewart", "Morris", "Reed", "Cooper", "Morgan", "Bennett",
    "Barnes", "Fisher", "Henderson", "Brooks", "Ross", "Hamilton", "Graham", "Price", "Fox", "West",
    "Sullivan", "Russell", "Wood", "Coleman", "Hayes", "Murphy", "Rivera", "Sanders", "Patterson", "Long",
    "Ford", "Butler", "Warren", "Gibson", "Spencer", "Gordon", "Wells", "Marshall", "Hunt", "Stone",
    "Grant", "Hudson", "Webb", "Crawford", "Burns", "Palmer", "Day", "Riley", "Owens", "Lane",
]

UK_MALE_FIRST = [
    "Oliver", "George", "Arthur", "Harry", "Jack", "Charlie", "Leo", "Oscar", "Freddie", "Archie",
    "Alfie", "Thomas", "Edward", "Henry", "Jacob", "Theo", "Noah", "Finley", "William", "Ethan",
    "Sebastian", "Rupert", "Hugo", "Felix", "Jasper", "Callum", "Liam", "Rory", "Miles", "Elliott",
    "Harvey", "Toby", "Harrison", "Angus", "Fergus", "Hamish", "Duncan", "Blair", "Alistair", "Reginald",
    "Nigel", "Colin", "Clive", "Graham", "Trevor", "Derek", "Stuart", "Keith", "Neville", "Cedric",
]

UK_FEMALE_FIRST = [
    "Olivia", "Amelia", "Isla", "Ava", "Emily", "Mia", "Sophia", "Grace", "Lily", "Freya",
    "Poppy", "Daisy", "Rosie", "Florence", "Willow", "Ivy", "Elsie", "Evie", "Sienna", "Phoebe",
    "Harriet", "Imogen", "Matilda", "Amelie", "Millie", "Eliza", "Martha", "Thea", "Alice", "Beatrice",
    "Pippa", "Penelope", "Fiona", "Gemma", "Nicola", "Victoria", "Charlotte", "Eleanor", "Georgina", "Philippa",
]

UK_LAST = [
    "Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Wilson", "Evans", "Thomas", "Johnson",
    "Roberts", "Walker", "Wright", "Robinson", "Thompson", "White", "Hughes", "Edwards", "Green", "Hall",
    "Lewis", "Harris", "Clarke", "Patel", "Jackson", "Wood", "Turner", "Martin", "Cooper", "Hill",
]

FRENCH_MALE_FIRST = [
    "Lucas", "Gabriel", "Leo", "Raphael", "Arthur", "Louis", "Jules", "Adam", "Hugo", "Liam",
    "Nathan", "Ethan", "Paul", "Noel", "Theo", "Sacha", "Tom", "Noah", "Enzo", "Mathis",
    "Alexandre", "Antoine", "Baptiste", "Clement", "Damien", "Emile", "Fabien", "Gregoire", "Henri", "Jacques",
]

FRENCH_FEMALE_FIRST = [
    "Emma", "Jade", "Louise", "Alice", "Chloe", "Lina", "Lea", "Rose", "Anna", "Mila",
    "Julia", "Manon", "Camille", "Ines", "Sarah", "Eva", "Zoe", "Lucie", "Clara", "Marie",
    "Amelie", "Aurelie", "Brigitte", "Caroline", "Delphine", "Eloise", "Florence", "Genevieve", "Helene", "Isabelle",
]

FRENCH_LAST = [
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau",
    "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier",
]

GERMAN_MALE_FIRST = [
    "Ben", "Paul", "Finn", "Leon", "Elias", "Jonas", "Noah", "Felix", "Luis", "Luca",
    "Maximilian", "Alexander", "Moritz", "Julian", "Sebastian", "Niklas", "Tobias", "Florian", "Lukas", "Jan",
]

GERMAN_FEMALE_FIRST = [
    "Emma", "Mia", "Hannah", "Sophia", "Emilia", "Lina", "Marie", "Mila", "Ella", "Clara",
    "Anna", "Lea", "Lena", "Johanna", "Luisa", "Charlotte", "Maja", "Sophie", "Amelie", "Nele",
]

GERMAN_LAST = [
    "Muller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
    "Schafer", "Koch", "Bauer", "Richter", "Klein", "Wolf", "Schroder", "Neumann", "Schwarz", "Zimmermann",
]

SPANISH_MALE_FIRST = [
    "Hugo", "Mateo", "Martin", "Lucas", "Leo", "Daniel", "Alejandro", "Pablo", "Manuel", "Alvaro",
    "Adrian", "David", "Mario", "Diego", "Javier", "Carlos", "Miguel", "Sergio", "Ivan", "Raul",
]

SPANISH_FEMALE_FIRST = [
    "Lucia", "Sofia", "Maria", "Martina", "Paula", "Julia", "Daniela", "Valeria", "Alba", "Emma",
    "Carla", "Sara", "Noa", "Carmen", "Claudia", "Valentina", "Adriana", "Alejandra", "Ana", "Elena",
]

SPANISH_LAST = [
    "Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Hernandez", "Perez", "Sanchez", "Ramirez", "Torres",
    "Flores", "Rivera", "Gomez", "Diaz", "Reyes", "Cruz", "Morales", "Ortiz", "Gutierrez", "Chavez",
]

ITALIAN_MALE_FIRST = [
    "Leonardo", "Francesco", "Alessandro", "Lorenzo", "Mattia", "Andrea", "Gabriele", "Riccardo", "Tommaso", "Edoardo",
    "Giuseppe", "Giovanni", "Marco", "Luca", "Stefano", "Roberto", "Antonio", "Massimo", "Vincenzo", "Paolo",
]

ITALIAN_FEMALE_FIRST = [
    "Sofia", "Giulia", "Aurora", "Alice", "Ginevra", "Emma", "Giorgia", "Greta", "Beatrice", "Anna",
    "Chiara", "Sara", "Francesca", "Elena", "Valentina", "Alessia", "Martina", "Elisa", "Arianna", "Bianca",
]

ITALIAN_LAST = [
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco",
    "Bruno", "Gallo", "Conti", "DeLuca", "Mancini", "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti",
]

AUSTRALIAN_MALE_FIRST = [
    "Jack", "Oliver", "William", "Noah", "James", "Thomas", "Henry", "Charlie", "Leo", "Lucas",
    "Liam", "Ethan", "Mason", "Alexander", "Ryan", "Cooper", "Archer", "Harrison", "Hunter", "Lachlan",
]

AUSTRALIAN_FEMALE_FIRST = [
    "Charlotte", "Olivia", "Amelia", "Isla", "Ava", "Mia", "Grace", "Willow", "Harper", "Chloe",
    "Ella", "Sophie", "Lily", "Zoe", "Emily", "Ruby", "Ivy", "Sienna", "Matilda", "Evelyn",
]

AUSTRALIAN_LAST = [
    "Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Johnson", "White", "Martin", "Anderson",
    "Thompson", "Nguyen", "Thomas", "Walker", "Harris", "Lee", "Ryan", "Robinson", "Kelly", "King",
]

# ==================== GENERATION FUNCTIONS ====================

def _pick_gender():
    """70% male, 30% female."""
    return "M" if random.random() < 0.70 else "F"


_ORIGIN_POOLS = {
    "indian": (INDIAN_MALE_FIRST, INDIAN_FEMALE_FIRST, INDIAN_LAST),
    "us":     (US_MALE_FIRST, US_FEMALE_FIRST, US_LAST),
    "uk":     (UK_MALE_FIRST, UK_FEMALE_FIRST, UK_LAST),
    "french":  (FRENCH_MALE_FIRST, FRENCH_FEMALE_FIRST, FRENCH_LAST),
    "german":  (GERMAN_MALE_FIRST, GERMAN_FEMALE_FIRST, GERMAN_LAST),
    "spanish": (SPANISH_MALE_FIRST, SPANISH_FEMALE_FIRST, SPANISH_LAST),
    "italian": (ITALIAN_MALE_FIRST, ITALIAN_FEMALE_FIRST, ITALIAN_LAST),
    "australian": (AUSTRALIAN_MALE_FIRST, AUSTRALIAN_FEMALE_FIRST, AUSTRALIAN_LAST),
}

_ORIGIN_CHOICES = ["indian", "us", "uk", "french", "german", "spanish", "italian", "australian"]
_ORIGIN_WEIGHTS = [10, 18, 15, 13, 12, 12, 10, 10]


def _pick_origin():
    """10% Indian, 90% international."""
    return random.choices(_ORIGIN_CHOICES, weights=_ORIGIN_WEIGHTS, k=1)[0]


def _pick_name(gender, origin):
    """Pick first+last name from same origin pool."""
    male_first, female_first, last_names = _ORIGIN_POOLS[origin]
    first = random.choice(male_first if gender == "M" else female_first)
    last = random.choice(last_names)
    return first, last


def _generate_dob(min_age=21, max_age=40):
    """Generate DOB between 21 and 40 years ago."""
    today = datetime.now()
    age = random.randint(min_age, max_age)
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)

    # Simple text DOB formatted
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    dob_str = f"{months[birth_month-1]} {birth_day:02d}, {birth_year}"
    return dob_str, birth_year


def _random_code(length=3):
    """Generate random alphanumeric code."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))


def _generate_email_username(first_name: str, last_name: str, birth_year: int) -> str:
    """Generate bulletproof username for Gmail."""
    fn = "".join(c for c in first_name.lower() if c.isalnum())
    ln = "".join(c for c in last_name.lower() if c.isalnum())

    yr = str(birth_year)[-2:]
    code2 = _random_code(2)
    code3 = _random_code(3)
    d2 = str(random.randint(10, 99))
    d3 = str(random.randint(100, 999))
    code4 = _random_code(4)

    patterns = [
        f"{fn}{ln}{d2}{code2}",
        f"{fn}{ln}{yr}{code2}",
        f"{fn}{ln}{code3}",
        f"{fn}{ln}{code4}",
        f"{fn[:2]}{ln}{yr}{code3}",
        f"{fn}{d3}{code2}",
        f"{fn}{ln}{birth_year}{code2}",
        f"{fn}.{ln}{d2}{code2}",
        f"{fn}.{ln}{yr}{code2}",
        f"{fn}.{ln}{code3}",
        f"{fn}.{ln}{birth_year}{code2}",
        f"{fn}{code3}{ln}",
        f"{fn}{d2}{ln}{code2}",
        f"{fn[:1]}{ln}{code4}",
    ]

    weights = [
        15, 15, 12, 10, 8, 5, 8,
        8, 8, 5, 3,
        1, 1, 1,
    ]

    return random.choices(patterns, weights=weights, k=1)[0]


def _generate_password(first_name: str, last_name: str, birth_year: int) -> str:
    """Generate strong but memorable password."""
    fn = first_name.capitalize()
    ln = last_name.capitalize()
    specials = ["@", "#", "$", "!", "&", "*"]
    spec = random.choice(specials)
    yr = str(birth_year)[-2:]
    num2 = str(random.randint(10, 99))
    num1 = str(random.randint(1, 9))
    letters = ''.join(random.choices(string.ascii_letters, k=2))

    patterns = [
        f"{fn}{spec}{yr}{num2}",
        f"{fn[:3]}{spec}{ln[:3]}{yr}{num1}",
        f"{ln}{spec}{fn[:2]}{num2}",
        f"{fn}{spec}{num2}{letters.upper()}",
        f"{fn[:4]}{ln[:2]}{spec}{yr}{num1}",
        f"{fn}{yr}{spec}{num2}",
        f"{ln[:3]}{fn[:3]}{spec}{num2}{num1}",
    ]

    return random.choice(patterns)


def generate_single_account(existing_emails: set) -> dict:
    """Generate a single random account block and ensure email is not in existing_emails."""
    for _ in range(50):
        gender = _pick_gender()
        origin = _pick_origin()
        first_name, last_name = _pick_name(gender, origin)
        dob_str, birth_year = _generate_dob(21, 40)
        email_user = _generate_email_username(first_name, last_name, birth_year)
        email = f"{email_user}@gmail.com"

        if email in existing_emails:
            continue

        password = _generate_password(first_name, last_name, birth_year)
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob_str,
            "gender": gender,
            "email": email,
            "password": password,
        }
    return None


def generate_accounts(count: int) -> list:
    """Generate multiple unique random accounts."""
    accounts = []
    generated_emails = set()

    for _ in range(count):
        acc = generate_single_account(generated_emails)
        if acc:
            generated_emails.add(acc["email"])
            accounts.append(acc)

    return accounts
