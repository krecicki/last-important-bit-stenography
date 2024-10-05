import numpy as np
from cryptography.fernet import Fernet
import os
from PIL import Image
import io
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

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, simple_key):
    key = derive_key(simple_key)
    f = Fernet(key)
    return f.encrypt(message.encode())

def hide_message(image_path, message, simple_key, output_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")
    
    # Open the image and convert to PNG format
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        
        # Save as PNG in memory
        png_buffer = io.BytesIO()
        img.save(png_buffer, format='PNG')
        png_buffer.seek(0)
        
        # Reopen the PNG image
        img = Image.open(png_buffer)
        width, height = img.size
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    encrypted_message = encrypt_message(message, simple_key)
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
    message_length = len(binary_message)
    
    if message_length > width * height * 3 - 32:
        raise ValueError("Message is too large for the image")
    
    # Flatten the image
    img_flat = img_array.flatten()
    
    # Store message length as 32-bit binary
    length_binary = format(message_length, '032b')
    for i, bit in enumerate(length_binary):
        img_flat[i] = (img_flat[i] & 0xFE) | int(bit)
    
    # Hide the message
    for i, bit in enumerate(binary_message):
        img_flat[i+32] = (img_flat[i+32] & 0xFE) | int(bit)
    
    # Reshape the image back to its original shape
    img_with_message = img_flat.reshape((height, width, 3))
    
    # Convert numpy array back to PIL Image and save as PNG
    Image.fromarray(img_with_message.astype('uint8'), 'RGB').save(output_path, 'PNG')
    
    print(f"Debug: Encrypted message length: {message_length}")
    print(f"Debug: First 50 bits of binary message: {binary_message[:50]}")
    print(f"Debug: Length binary: {length_binary}")

# Example usage
if __name__ == "__main__":
    simple_key = "mynameiscody"  # Can be any string now
    print(f"Using simple key: {simple_key}")
    
    input_image = "flarp.jpg"  # Can be any image format
    output_image = "output.png"  # Will always be PNG
    secret_message = "Cody likes to make things."
    
    try:
        hide_message(input_image, secret_message, simple_key, output_image)
        print(f"Message hidden in {output_image}")
    except Exception as e:
        print(f"An error occurred during message hiding: {str(e)}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())

    print("\nDebugging Information:")
    print(f"Input image exists: {os.path.exists(input_image)}")
    print(f"Output image exists: {os.path.exists(output_image)}")
    if os.path.exists(output_image):
        print(f"Input image size: {os.path.getsize(input_image)} bytes")
        print(f"Output image size: {os.path.getsize(output_image)} bytes")
