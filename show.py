import numpy as np
from cryptography.fernet import Fernet
import os
from PIL import Image
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(simple_key):
    salt = b'static_salt'  # In a real application, use a random salt and store it
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(simple_key.encode()))
    return key

def decrypt_message(encrypted_message, simple_key):
    key = derive_key(simple_key)
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def extract_message(image_path, simple_key):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")
    
    # Open the image
    with Image.open(image_path) as img:
        img_array = np.array(img)
    
    img_flat = img_array.flatten()
    
    length_bits = ''.join(str(byte & 1) for byte in img_flat[:32])
    message_length = int(length_bits, 2)
    
    print(f"Debug: Extracted length bits: {length_bits}")
    print(f"Debug: Extracted message length: {message_length}")
    
    if message_length > len(img_flat) - 32 or message_length <= 0:
        raise ValueError(f"Invalid message length: {message_length}")
    
    message_bits = ''.join(str(byte & 1) for byte in img_flat[32:32+message_length])
    
    print(f"Debug: First 50 bits of extracted message: {message_bits[:50]}")
    
    message_bytes = bytes(int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8))
    
    print(f"Debug: First 20 bytes of message_bytes: {message_bytes[:20]}")
    
    return decrypt_message(message_bytes, simple_key)

# Example usage
if __name__ == "__main__":
    simple_key = "mynameiscody"  # Can be any string now
    output_image = "output.png"  # The image with the hidden message
    
    try:
        extracted_message = extract_message(output_image, simple_key)
        print(f"Extracted message: {extracted_message}")
    except Exception as extract_error:
        print(f"Error during message extraction: {str(extract_error)}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
