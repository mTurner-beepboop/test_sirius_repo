import json

with open('temp.json', 'r') as file:
    data = json.load(file)

filtered_data = []

for item in data:
    filtered_data.append({'title':item['title'], 'authors':item['authors'], 'publication':item['publication'], 'year':item['year']})

print(filtered_data)