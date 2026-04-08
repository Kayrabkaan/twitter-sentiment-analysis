import csv
import re
import pandas as pd

    
def clean(file):
    return re.sub(r'[^\w\s]', '', file)
def clean_file(file):
    return re.sub(r'[_]','',file)
with open('twitter_training.csv', 'r', encoding='utf-8') as file_in, \
     open('cleaned_dataset.csv', 'w', newline='', encoding='utf-8') as file_out:

    reader = csv.reader(file_in)
    writer = csv.writer(file_out)
    
    for row in reader:
        cleaned_row = [clean(column) for column in row]
        writer.writerow(cleaned_row)

def clean_whitespace(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as file_out:
        
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        
        for row in reader:
            cleaned_row = [cell.strip() if isinstance(cell, str) else cell for cell in row]
            writer.writerow(cleaned_row)


clean_whitespace('cleaned_dataset.csv', 'cleaned_dataset_1.csv')
def clean_empty_row(input_file, output_file):
    
    data = pd.read_csv(input_file)

    cleaned_data = data.dropna()
     
    cleaned_data.to_csv(output_file, index=False, encoding='utf-8')

clean_empty_row('cleaned_dataset_1.csv', 'cleaned_dataset_2.csv')        
