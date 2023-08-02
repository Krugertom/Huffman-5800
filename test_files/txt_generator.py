import random
import string
import requests

def generate_random_txt(file_count, min_char, max_char):
    
    increments = max_char // file_count
    count = 0
    for i in range(file_count):
        count += 1
        current_length = min_char + i * increments
        if current_length > max_char:
            current_length = max_char
        
        print(count)

        text = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(current_length))
        
        # Adding new line break after every 100 characters
        text_with_breaks = '\n'.join(text[i:i+100] for i in range(0, current_length, 100))
        
        with open(f"test_files/infile_test_{i}.txt", "w") as f:
            f.write(text_with_breaks)

def generate_shakespeare_txt(file_count, min_char, max_char):
    increments = max_char // file_count
    url = "https://www.gutenberg.org/files/1787/1787.txt"

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to download Hamlet")
        return

    shakespeare_text = response.text.split("SCENE.- Elsinore.")[1]  # Use the part after "SCENE.- Elsinore."

    for i in range(file_count):
        current_length = min_char + i * increments
        if current_length > max_char:
            current_length = max_char

        # Truncate or repeat the text to fit the desired length
        text = (shakespeare_text * ((current_length // len(shakespeare_text)) + 1))[:current_length]
        
        # Adding new line break after every 100 characters
        text_with_breaks = '\n'.join(text[i:i+100] for i in range(0, current_length, 100))
        
        with open(f"test_files/infile_test_shakespeare_{i}.txt", "w") as f:
            f.write(text_with_breaks)

def main():
    # -------- TEST ATTRIBUTES ------------
    file_count = 15
    min_char = 100
    max_char = 10000000
    
    # -------- APP DRIVER -----------------
    generate_random_txt(file_count, min_char, max_char)
    generate_shakespeare_txt(file_count, min_char, max_char)
    
if __name__ == "__main__":
    main()
