import pandas as pd


athletes = pd.read_csv('/Users/Kathi/Downloads/paralympics/paralympic-athletes.csv')
coaches = pd.read_csv('/Users/Kathi/Downloads/paralympics/paralympic-coaches.csv')


# seperate last name from first name

full_names = athletes['Name']

test = full_names

output_firstname = []
output_lastname = []

for name in test:
    words = name.split()
    lastname = ''
    firstname = ''
    for word in words:  
        if word.isupper():
            lastname = lastname + " " + word
        else:
            firstname = firstname + " " + word
    output_firstname.append(firstname)
    output_lastname.append(lastname)


#print(output_firstname)
#print(output_lastname)

# turn Female and Male into F and M

athletes['Gender'] = athletes['Gender'].replace({'Female':'F', 'Male':'M'})

# add new columns for First and Last Name

athletes['First Name'] = output_firstname
athletes['Last Name'] = output_lastname

# drop full name
athletes = athletes.drop(columns=['Name'])

athletes.to_csv('athletes-preprocessed.csv')
print(athletes)