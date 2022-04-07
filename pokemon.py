import csv
from collections import defaultdict
from collections import Counter

def pokemon1(f):
    reader = csv.DictReader(open(f))
    num = 0
    fire = 0
    for index,row in enumerate(reader):
        if (row['type'] == 'fire'):
            fire += 1
            if(float(row['level']) >= 40):
                num+= 1
    avg = round((num/fire) * 100)
    outfile = open("pokemon1.txt","w")
    outfile.write("Percentage of fire type Pokemons at or above level 40 = " + str(avg))
    outfile.close()

def weaknessDictionary(f):
    typeDict = defaultdict(list)
    reader = csv.DictReader(open(f))
    for index, row in enumerate(reader):
        if (row['type'] != 'NaN'):
            typeDict[(row['weakness'])].append(row['type'])
    typeDict = dict(typeDict)
    typeDict = dict(sorted(typeDict.items()))
    weaknessDict = {}
    for weakness, pokeTypes in typeDict.items():
        pokeType = Counter(pokeTypes)
        weaknessDict[weakness] = pokeType.most_common()[0][0]
    return weaknessDict

def statDictionary(f):
    below40 = defaultdict(list)
    above40 = defaultdict(list)
    reader = csv.DictReader(open(f))
    for index, row in enumerate(reader):
        if(float(row['level']) <= 40):
            if(row['atk'] != 'NaN'):
                below40['atk'].append(float(row['atk']))
            if(row['def'] != 'NaN'):
                below40['def'].append(float(row['def']))
            if(row['hp'] != 'NaN'):
                below40['hp'].append(float(row['hp']))
        else:
            if(row['atk'] != 'NaN'):
                above40['atk'].append(float(row['atk']))
            if(row['def'] != 'NaN'):
                above40['def'].append(float(row['def']))
            if(row['hp'] != 'NaN'):
                above40['hp'].append(float(row['hp']))
    below40avgATK = round(sum(below40['atk'])/len(below40['atk']),1)
    below40avgDEF = round(sum(below40['def'])/len(below40['def']),1)
    below40avgHP = round(sum(below40['hp'])/len(below40['hp']),1)
    below40avgs = dict(zip(['atk','def','hp'],[below40avgATK,below40avgDEF,below40avgHP]))

    above40avgATK = round(sum(above40['atk'])/len(above40['atk']),1)
    above40avgDEF = round(sum(above40['def'])/len(above40['def']),1)
    above40avgHP = round(sum(above40['hp'])/len(above40['hp']),1)
    above40avgs = dict(zip(['atk','def','hp'],[above40avgATK,above40avgDEF,above40avgHP]))
    return below40avgs,above40avgs

def pokemon23(f,weaknessDict,below40avgs,above40avgs):
    with open(f) as pokemonTrain: 
        reader = csv.DictReader(pokemonTrain)

        with open('pokemonResult.csv','w',newline='') as pokemonResult:
            # fieldnames is a required parameter for DictWriter
            writer = csv.DictWriter(pokemonResult,fieldnames=reader.fieldnames, delimiter=',')  
            writer.writeheader()   
            for row in reader:
                if(row['type']=='NaN'):
                    row['type']=weaknessDict[row['weakness']]
                if(float(row['level']) <= 40):
                    if(row['atk'] == 'NaN'):
                        row['atk'] = below40avgs['atk']
                    if(row['def'] == 'NaN'):
                        row['def'] = below40avgs['def']
                    if(row['hp'] == 'NaN'):
                        row['hp'] = below40avgs['hp']
                else:
                    if(row['atk'] == 'NaN'):
                        row['atk'] = above40avgs['atk']
                    if(row['def'] == 'NaN'):
                        row['def'] = above40avgs['def']
                    if(row['hp'] == 'NaN'):
                        row['hp'] = above40avgs['hp']
                writer.writerow(row)   
    pokemonResult.close()

def pokemon4(f):
    reader = csv.DictReader(open(f))
    natures = defaultdict(list)
    for index,row in enumerate(reader):
        if(row['personality'] not in natures[row['type']]):
            natures[row['type']].append(row['personality'])
    natures = dict(natures)

    for pType,personalities in natures.items():
        personalities.sort()
    natures=dict(sorted(natures.items()))
    outfile = open("pokemon4.txt","w")
    outfile.write("Pokemon type to personality mapping: \n")
    for pType,personalities in natures.items():
        outfile.write(f"\t" + pType + ": " + ", ".join(personalities)  + "\n")
    outfile.close() 
    
def pokemon5(f):
    reader = csv.DictReader(open(f))
    num = 0
    hp = 0
    for index,row in enumerate(reader):
        if (row['stage'] == '3.0'):
            num+=1
            hp+=float(row['hp'])
    avg = round((hp/num),1)
    outfile = open("pokemon5.txt","w")
    outfile.write("Average hit point for Pokemons of stage 3.0 = " + str(avg))
    outfile.close()

def main():
    pokemon1("pokemonTrain.csv")
    wDict = weaknessDictionary("pokemonTrain.csv")
    b40,a40 = statDictionary("pokemonTrain.csv")
    pokemon23("pokemonTrain.csv",wDict,b40,a40)
    pokemon4("pokemonResult.csv")
    pokemon5("pokemonResult.csv")

main()