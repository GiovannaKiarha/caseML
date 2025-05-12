import csv #abrir o arquivo csv
from math import radians, cos, sin, asin, sqrt #realizar o cálculo de haversine

#haversine vai ser utilizado aqui pois leva em consideração a curvatura da terra, usa os dados que foram dados E JÁ COLOCA EM KM. Sendo assim, eu não preciso fazer outra função só para isso

def calculate_distance(lon1, lat1, lon2, lat2): 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    distancia_lon = lon2 - lon1 
    distancia_lat = lat2 - lat1 
    a = sin(distancia_lat/2)**2 + cos(lat1) * cos(lat2) * sin(distancia_lon/2)**2
    c = 2 * asin(sqrt(a)) # raiz quadrada
    r = 6371 #raio da terra aproximadamente
    return c * r

def validate_coordinates(row): # precisa validar os dados pois tem muitos dados nulos na tabela que foi passada (pode ser feito com pandas também, mas aqui deixaria o código mais curto)
    if row['start_lng'] == '':
        return False
    if row['start_lat'] == '':
       return False
    if row['end_lng'] == '':
       return False
    if row['end_lat'] == '':
       return False
    if row['start_lng'] == 'null':
        return False
    if row['end_lng'] == 'null':
        return False
    if row['start_lat'] == 'null':
        return False
    if row['end_lat'] == 'null':
        return False
    return True

csv_len = 0 #tamanho do csv
total_duration = 0 #total de todas as durações do csv de treinamento
total_distance = 0 #total de todas as distâncias
with open("train.csv") as train:
    data = csv.DictReader(train)

    with open('submission.csv', 'a', newline='') as submission:
        writer = csv.DictWriter(submission, fieldnames = ["row_id", "duration"])
        writer.writeheader()

    for row in data:
        if float(row['duration']) < 0.01:
            print('Duração inválida menor que 0.01')
            continue

        if validate_coordinates(row) == False:
            continue

        #No python precisa especificar que seria float, se não, tentaria colocar como str, travaria os cálculos e não levaria em consideração os decimais
        start_lng = float(row['start_lng']) 
        start_lat = float(row['start_lat'])
        end_lng = float(row['end_lng'] )
        end_lat = float(row['end_lat'])
        
        distance = calculate_distance(start_lng, start_lat, end_lng, end_lat)
        speed_kph = distance / (float(row['duration']) / 3600)

        if (speed_kph > 300): #existem valores na tabela que ultrapassam o valor de 300km/h, o que acaba prejudicando o código e não fazendo rodar
            print('Velocidade inválida maior que 300 km/h')
            continue

        csv_len += 1
        total_distance += distance
        total_duration += float(row['duration'])
        print(f"[Row Id] > {row['row_id']} [Average Speed] > {speed_kph:.2f} km/h", f" [Distance] > {distance}", f" [Duration] > {row['duration']}")    

        with open('submission.csv', 'a', newline='') as submission: #aqui abre o arquivo submission que foi passado e cria as duas colunas pedidas no desafio e preenche automaticamente(poderia ser feito com pandas também)
            submission.write(f"{row['row_id']}, {row['duration']}\n")

    duration_hours = total_duration / 3600.0
    speed_kph = total_distance / duration_hours

    print(f'[Total Distance in km] > {total_distance:.2f}')
    print(f'[Total Duration in seconds] > {total_duration:.2f}')
    print(f'[Average Speed] > {speed_kph:.2f} km/h')

    print("Arquivo 'submission.csv' gerado com base apenas na distância e velocidade média.")
