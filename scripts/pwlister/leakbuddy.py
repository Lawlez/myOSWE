import os
import zipfile

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def user_confirm_overwrite(file_path):
    return input(f'The file {file_path} already exists. Overwrite? (y/n): ').lower() == 'y'

def remove_duplicates(strings):
    seen = set()
    seen_add = seen.add
    duplicates_removed = len(strings) - len(set(strings))
    return [x for x in strings if not (x in seen or seen_add(x))], duplicates_removed

def process_extracted_file(file_name, all_filtered_strings):
    try:
        # Attempt to open the file with UTF-8 encoding
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        # If a UnicodeDecodeError occurs, try ISO-8859-1 encoding
        with open(file_name, 'r', encoding='iso-8859-1') as file:
            lines = file.readlines()

    # Extract and store the desired part of each line
    filtered_strings = [line.split(':')[-1].strip() for line in lines]
    all_filtered_strings.extend(filtered_strings)

    return len(lines)  # Return the number of processed lines for logging

def unzip_and_filter_files(output_file_name):
    ensure_directory_exists('./out')
    output_file_path = f'./out/{output_file_name}'
    
    if os.path.exists(output_file_path) and not user_confirm_overwrite(output_file_path):
        print("Operation cancelled by user.")
        return
    
    total_processed_lines = 0
    all_filtered_strings = []
    
    for file_name in os.listdir('.'):
        if file_name.endswith('.txt.zip'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall('.')
                
                for extracted_file in zip_ref.namelist():
                    processed_lines = process_extracted_file(extracted_file, all_filtered_strings)
                    total_processed_lines += processed_lines
                    
                    os.remove(extracted_file)

    # Remove duplicates and count them
    unique_strings, duplicates_removed = remove_duplicates(all_filtered_strings)

    # Write the unique strings to the file
    with open(output_file_path, 'w') as out_file:
        for string in unique_strings:
            out_file.write(string + '\n')

    print(f'All files have been processed. Output available in {output_file_path}')
    print(f'Total lines processed: {total_processed_lines}')
    print(f'Duplicates removed: {duplicates_removed}')

unzip_and_filter_files('RU-2024.txt')
