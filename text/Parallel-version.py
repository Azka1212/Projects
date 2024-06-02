import multiprocessing


def sanitize_text(text):
    # Placeholder function to sanitize text data
    # You can customize this function as per your sanitization requirements
    sanitized_text = text.replace("sensitive_word", "***SANITIZED***")
    return sanitized_text


def parallel_text_sanitization(texts):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    sanitized_texts = pool.map(sanitize_text, texts)
    pool.close()
    pool.join()
    return sanitized_texts


if __name__ == "__main__":
    # Example dataset (list of texts)
    texts = [
        "This is a sensitive document containing sensitive_word.",
        "Another sensitive information: sensitive_word123.",
    ]

    # Parallel text sanitization
    parallel_sanitized_texts = parallel_text_sanitization(texts)

    # Print sanitized texts
    print("Parallel Sanitized Texts:")
    for idx, sanitized_text in enumerate(parallel_sanitized_texts):
        print(f"Text {idx + 1}: {sanitized_text}")
