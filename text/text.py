import multiprocessing

def sanitize_text(text):
    # Placeholder function to sanitize text data
    # You can customize this function as per your sanitization requirements
    sanitized_text = text.replace('sensitive_word', '***SANITIZED***')
    return sanitized_text

def serial_text_sanitization(texts):
    sanitized_texts = []
    for text in texts:
        sanitized_text = sanitize_text(text)
        sanitized_texts.append(sanitized_text)
    return sanitized_texts

def parallel_text_sanitization(texts):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    sanitized_texts = pool.map(sanitize_text, texts)
    pool.close()
    pool.join()
    return sanitized_texts

if __name__ == '__main__':
    # File path to the input text file
    input_file_path = r'C:\Users\Azka\Desktop\text\input_texts.txt'
    
    # Read text data from the file
    with open(input_file_path, 'r') as file:
        texts = file.readlines()
    
    # Serial text sanitization
    serial_sanitized_texts = serial_text_sanitization(texts)
    
    # Parallel text sanitization
    parallel_sanitized_texts = parallel_text_sanitization(texts)
    
    # Print sanitized texts
    print("Serial Sanitized Texts:")
    for idx, sanitized_text in enumerate(serial_sanitized_texts):
        print(f"Text {idx + 1}: {sanitized_text.strip()}")
    
    print("\nParallel Sanitized Texts:")
    for idx, sanitized_text in enumerate(parallel_sanitized_texts):
        print(f"Text {idx + 1}: {sanitized_text.strip()}")
