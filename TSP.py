import xml.etree.ElementTree as ET
import random, math

def get_orase(path):
    tree = ET.parse(path)
    root = tree.getroot()

    cities = []
    for row in root.findall("row"):
        city_id = int(row.find("City").text)
        x = float(row.find("X").text)
        y = float(row.find("Y").text)
        cities.append({"id": city_id, "x": x, "y": y})
    return cities

def init_populatie(orase, size):
    id_orase = [city["id"] for city in orase]
    populatie = []

    for _ in range(size):
        individ = id_orase.copy()
        random.shuffle(individ)
        individ.append(individ[0])
        populatie.append(individ)
    return populatie

def distanta_euclidiana(a, b):
    return math.sqrt((a["x"] - b["x"])**2 + (a["y"] - b["y"])**2)

def fitness(individ, orase_dict):
    distanta_totala = 0
    for i in range(len(individ)-1):
        oras_curent = orase_dict[individ[i]]
        oras_urmator = orase_dict[individ[(i + 1) % len(individ)]]
        distanta_totala += distanta_euclidiana(oras_curent, oras_urmator)
    return distanta_totala

def selectie(populatie):
    return random.sample(populatie, 2)

def crossover(parinte1, parinte2):
    lungime = len(parinte1)-1
    poz1, poz2 = sorted(random.sample(range(lungime), 2))

    def copil_nou(segment_parinte, completare_parinte, poz1, poz2):
        copil = [None] * lungime
        copil[poz1:poz2 + 1] = segment_parinte[poz1:poz2 + 1]
        #print(f"segment copiat: {copil[poz1:poz2 + 1]}")

        index = 0
        for i in range(lungime):
            if copil[i] is None:
                while completare_parinte[index] in copil:
                    index += 1
                copil[i] = completare_parinte[index]
        copil.append(copil[0])
        return copil

    copil1 = copil_nou(parinte1, parinte2, poz1, poz2)
    copil2 = copil_nou(parinte2, parinte1, poz1, poz2)
    
    return copil1, copil2

cities = get_orase("tsp.xml")[:100]
population = init_populatie(cities, 10)
orase_dict = {oras["id"]: oras for oras in cities}

parinte1, parinte2 = selectie(population)
copil1, copil2 = crossover(parinte1, parinte2)

print("Părinte 1:", parinte1)
print("Părinte 2:", parinte2)
print("Copil 1  :", copil1)
print("Copil 2  :", copil2)
print("Fitness Părinte 1:", fitness(parinte1, orase_dict))
print("Fitness Părinte 2:", fitness(parinte2, orase_dict))
print("Fitness Copil 1  :", fitness(copil1, orase_dict))
print("Fitness Copil 2  :", fitness(copil2, orase_dict))