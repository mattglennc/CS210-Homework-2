import csv
from collections import defaultdict
from collections import Counter

def changeDate(date):
    dates = date.split('.')
    return '.'.join([dates[1],dates[0],dates[2]])

def coordDictionary(f):
    latitudes = defaultdict(list)
    longitudes = defaultdict(list)
    reader = csv.DictReader(open(f))
    for index, row in enumerate(reader):
        if row['latitude'] != 'NaN':
            latitudes[row['province']].append(float(row['latitude']))
        if row['longitude'] != 'NaN':
            longitudes[row['province']].append(float(row['longitude']))
    latitudes = [(province,sum(lats)/len(lats)) for province,lats in latitudes.items()]
    longitudes = [(province,sum(longs)/len(longs)) for province,longs in longitudes.items()]
    return dict(latitudes),dict(longitudes)

def cityDict(f):
    cityDictionary = {}
    province_to_city = defaultdict(list)
    reader = csv.DictReader(open(f))
    for index, row in enumerate(reader):
        if row['city'] != 'NaN':
            province_to_city[row['province']].append(row['city'])
    for province, cities in province_to_city.items():
        cityCounts = Counter(cities)
        cityDictionary[province] = cityCounts.most_common()[0][0]
    return dict(sorted(cityDictionary.items()))

def symptomDict(f):
    symptomDictionary = {}
    province_to_symptom = defaultdict(list)
    reader = csv.DictReader(open(f))
    for index, row in enumerate(reader):
        if row['symptoms'] != 'NaN':
            symptomList = row['symptoms'].split(';');
            symptomList2 = []
            symptomList2.extend([word.strip(' ') for word in symptomList])
            province_to_symptom[row['province']].extend(symptomList2)
    for province, symptoms in province_to_symptom.items():
        sympCounts = Counter(symptoms)
        symptomDictionary[province] = sympCounts.most_common()[0][0]
    return dict(sorted(symptomDictionary.items()))


def problem2(f):
    reader = csv.DictReader(open(f))
    with open('covidResult.csv','w',newline='') as covidResult:
            writer = csv.DictWriter(covidResult,fieldnames=reader.fieldnames, delimiter=',')  
            writer.writeheader() 
            latDict,longDict = coordDictionary(f)
            cityD = cityDict(f)
            symptomD = symptomDict(f)
            for index,row in enumerate(reader):
                #2.1
                ages = row['age'].split("-")
                ages = [int(age) for age in ages]
                row['age'] = round(sum(ages)/len(ages))
                #2.2
                for key in row.keys():
                    if 'date' in key:
                        row[key] = changeDate(row[key])
                #2.3
                if (row['latitude'] == 'NaN'):
                    row['latitude'] = round(latDict[row['province']],2)
                if(row['longitude'] == 'NaN'):
                    row['longitude'] = round(longDict[row['province']],2)
                #2.4
                if (row['city'] == 'NaN'):
                    row['city'] = cityD[row['province']]
                #2.5
                if (row['symptoms'] == 'NaN'):
                    row['symptoms'] = symptomD[row['province']]
                writer.writerow(row)
    covidResult.close()




def main():
    problem2("covidTrain.csv")

main()