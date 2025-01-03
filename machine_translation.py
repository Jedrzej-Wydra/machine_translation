import spacy
import re
import openai
import markdown
import os

date_pattern = r"\b\d{2}\.\d{2}\.\d{4}\b"

print("Enter the api key: ")
openai_key = input()

print("Enter the file path: ")
path = input()

print("Enter the language you want to translate to: ")
lang_to = input()

client = openai.OpenAI(api_key=openai_key)

#def flatten_list(nested_list):
#    flattened = []
#    for item in nested_list:
#        if isinstance(item, list): 
#            flattened.extend(flatten_list(item))
#        else:
#            flattened.append(item)
#    return flattened

def modify_path(path, new_ext):
    directory, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)

    new_name = f"{name}_translated"
    modified_filename = f"{new_name}{new_ext}"

    return os.path.join(directory, modified_filename)

nlp = spacy.load("xx_ent_wiki_sm")
#nlp = spacy.load("es_core_news_sm")

with open(path, "r", encoding="utf-8") as file:
    text = file.read()

text = text.replace("\n", " \n ")
doc = nlp(text)

#entities = {'persName': [], 
#            'orgName': [], 
#            'placeName': []}

#for ent in doc.ents:
#    if ent.label_ in list(entities.keys()):
#        entities[ent.label_].append(ent.text)

#entities = {label: list(set(values)) for label, values in entities.items()}

#id_number = iter(list(range(345,999)))
#for key in entities.keys():
#    for i in range(len(entities[key])):
#        temp_list = entities[key][i]
#        entities[key][i] = []
#        for j in list(temp_list.split()):
#            entities[key][i].append((j, ' ENT' + str(next(id_number)) + ' '))
        
pattern = r"\b\d{11}"
matches = re.findall(pattern, text)

replacements = []

for i, match in enumerate(matches, start=1):
    placeholder = f"PSLS{i}"
    text = text.replace(match, placeholder) 
    replacements.append((match, placeholder))  
    
matches = re.findall(date_pattern, text)

replacements2 = []

for i, match in enumerate(matches, start=1):
    placeholder = f"DTS{i}"
    text = text.replace(match, placeholder) 
    replacements2.append((match, placeholder))
    
pattern = r"\d{4}" 
matches = re.findall(pattern, text)

replacements3 = []

for i, match in enumerate(matches, start=1):
    placeholder = f"NBRS{i}"
    text = text.replace(match, placeholder) 
    replacements3.append((match, placeholder)) 
    
id_number = iter(list(range(345,9999)))
entities = []
for ent in doc.ents:
    for spl in ent.text.split():
        if len(spl) > 1:
            entities.append((spl,  ' ENT' + str(next(id_number)) + ' '))
            entities.append((spl.lower(),  ' ENT' + str(next(id_number)) + ' '))
            entities.append((spl.upper(),  ' ENT' + str(next(id_number)) + ' '))
            entities.append((spl.capitalize(),  ' ENT' + str(next(id_number)) + ' '))
    
for old, new in entities:
    text = text.replace(old, new)
    
prompt = f"You are an expert in the grammar of the language in which the provided text is written. Do not modify words that start with 'ENT', 'PSLS', 'DTS' and 'NBRS'. Correct the text enclosed in brackets [ ] and format it in markdown with proper paragraph divisions, appropriate titles, and typographic correctness. Provide only the corrected text, without adding any comments or explanations. [{text}]"

chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                    }
                ],
            model="gpt-4o"
            )

text = chat_completion.choices[0].message.content

prompt = f"Translate the text enclosed in brackets [ ] to {lang_to}, and format it in markdown with proper paragraph divisions, appropriate titles, and typographic correctness. Do not add anything extra; provide only the transformed text without comments or explanations. [{text}]"    
    
chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                    }
                ],
            model="gpt-4o"
            )

text = chat_completion.choices[0].message.content

anonim = text

entities = [(' ' + t[0] + ' ', t[1].strip()) for t in entities]

for old, new in entities:
    text = text.replace(new, old)
        
for rep1, rep2 in replacements:
    text = text.replace(rep2, rep1)
    
for rep1, rep2 in replacements2:
    text = text.replace(rep2, rep1)

for rep1, rep2 in replacements3:
    text = text.replace(rep2, rep1)
    
text = text.replace("  ", " ")
text = text.replace(" , ", ", ")
text = text.replace(" . ", ". ")
    
html_content = markdown.markdown(text)
html_content_2 = markdown.markdown(anonim)

html_file_name = modify_path(path, '.html')
html_file_name2 = modify_path(path, '_A.html')

with open(html_file_name, "w", encoding="utf-8") as file:
    file.write(html_content)
    
with open(html_file_name2, "w", encoding="utf-8") as file:
    file.write(html_content_2)
    
print(f"Translated document saved to {html_file_name}")
print(f"Translated document saved to {html_file_name2}")