def sanitize_text(text):
    # Placeholder function to sanitize text data
    # You can customize this function as per your sanitization requirements
    sanitized_text = text.replace("sensitive_word", "***SANITIZED***")
    return sanitized_text


def serial_text_sanitization(texts):
    sanitized_texts = []
    for text in texts:
        sanitized_text = sanitize_text(text)
        sanitized_texts.append(sanitized_text)
    return sanitized_texts


if __name__ == "__main__":
    # Example dataset (list of texts)
    texts = [
        "This is a sensitive document containing sensitive_word.",
        "Another sensitive information: sensitive_word123.",
    ]

    # Serial text sanitization
    serial_sanitized_texts = serial_text_sanitization(texts)

    # Print sanitized texts
    print("Serial Sanitized Texts:")
    for idx, sanitized_text in enumerate(serial_sanitized_texts):
        print(f"Text {idx + 1}: {sanitized_text}")
