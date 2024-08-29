import os
import random
import glob
import string

min_size_mb = 1
max_size_mb = 12
def generate_random_text(size_bytes):
    # Define the character set (letters and digits)
    characters = string.ascii_letters + string.digits
    # Generate a string of the specified size
    return ''.join(random.choice(characters) for _ in range(size_bytes))

def delete_old_files():
    # Delete files matching the pattern "file*.txt"
    old_files = glob.glob("file*.txt")
    for file in old_files:
        os.remove(file)
        print(f"Deleted previously generated file: {file}")
                
def create_files(file_count):
    for i in range(file_count):
        size_mb = random.randint(min_size_mb, max_size_mb)
        size_bytes = size_mb * 1024 * 1024
        file_name = f"file{i + 1}.txt"
        content = generate_random_text(size_bytes).encode('utf-8')

        with open(file_name, 'wb') as f:
            f.write(content)
        
        print(f"Created {file_name} of size {size_mb} MB")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Missing argument: python create_files.py <file_count>")
    else:
        try:
            file_count = int(sys.argv[1])
            if file_count > 0 and file_count < 11:
                delete_old_files()
                create_files(file_count)
            else:
                print("Number of files should be between 1 and 10.")
        except ValueError:
            print("Please provide a valid integer.")
