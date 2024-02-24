import os
import zipfile

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def unzip_and_filter_files(output_file_name):
    # Ensure the output directory exists
    ensure_directory_exists('./out')
    
    total_processed_lines = 0  # Initialize counter for processed lines
    
    for file_name in os.listdir('.'):
        if file_name.endswith('.txt.zip'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall('.')
                
                # Process each extracted file
                for extracted_file in zip_ref.namelist():
                    processed_lines = process_extracted_file(extracted_file, output_file_name)
                    total_processed_lines += processed_lines
                    
                    # Remove the extracted file after processing
                    os.remove(extracted_file)

    print(f'All files have been processed. Output available in /out/{output_file_name}')
    print(f'Total lines processed: {total_processed_lines}')

def process_extracted_file(file_name, output_file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Filter lines, considering only the part after the last colon
    filtered_strings = [line.split(':')[-1].strip() for line in lines]

    # Write to new file
    with open(f'./out/{output_file_name}', 'a') as out_file:
        for string in filtered_strings:
            out_file.write(string + '\n')

    return len(filtered_strings)  # Return the number of processed lines for logging

unzip_and_filter_files('output.txt')
