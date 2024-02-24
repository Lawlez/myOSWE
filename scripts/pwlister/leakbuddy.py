import os
import zipfile

def unzip_and_filter_files(output_file_name):
    # Step 1: Identify and unzip .zip files
    for file_name in os.listdir('.'):
        if file_name.endswith('.txt.zip'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall('.')

                # Process each extracted file
                for extracted_file in zip_ref.namelist():
                    process_extracted_file(extracted_file, output_file_name)
                    
                    # Remove the extracted file after processing
                    os.remove(extracted_file)

    print(f'All files have been processed. Output available in /out/{output_file_name}')

def process_extracted_file(file_name, output_file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Step 2: Filter lines
    filtered_strings = [line.split(':')[1].strip() for line in lines]

    # Step 3: Write to new file
    with open(f'out/{output_file_name}', 'a') as out_file:
        for string in filtered_strings:
            out_file.write(string + '\n')

unzip_and_filter_files('output.txt')
