# Hide and Extract Messages in Images

This project provides two scripts, `hide.py` and `show.py`, to hide and extract encrypted messages in image files. Messages are encrypted using the **Fernet** symmetric encryption system, and the encrypted message is hidden in an image using steganography.

## Prerequisites

Ensure you have the following Python packages installed:

```bash
pip install numpy cryptography pillow
```

## How to Use

### 1. Hiding a Message (`hide.py`)

This script hides an encrypted message in an image file.

#### Example Usage:

```bash
python hide.py
```

#### Parameters:
- **input_image**: The image in which the message will be hidden (supports multiple formats, but output will be PNG).
- **output_image**: The name of the output image file with the hidden message (PNG format).
- **secret_message**: The message to be hidden.
- **simple_key**: A simple string used to derive the encryption key.

#### Output:
The image with the hidden message is saved as a PNG file in the specified `output_image`.

#### Debug Info:
- Encrypted message length.
- First 50 bits of the binary message.
- Length binary.

#### Example:

```bash
Using simple key: mynameiscody
Message hidden in output.png
```

### 2. Extracting a Message (`show.py`)

This script extracts and decrypts the hidden message from an image file.

#### Example Usage:

```bash
python show.py
```

#### Parameters:
- **output_image**: The image file containing the hidden message (PNG format).
- **simple_key**: The same string that was used to hide the message.

#### Output:
The extracted and decrypted message will be displayed.

#### Debug Info:
- Extracted length bits.
- Extracted message length.
- First 50 bits of the extracted message.

#### Example:

```bash
Extracted message: Cody likes to code.
```

## How It Works

### Hiding a Message
1. The message is encrypted using a simple key-derived encryption key.
2. The encrypted message is converted to binary and hidden in the image pixels.
3. The size of the hidden message is also stored in the image.

### Extracting a Message
1. The size of the hidden message is extracted from the image.
2. The hidden binary message is extracted from the pixels.
3. The binary message is converted back to bytes and decrypted using the same key.

## Important Notes
- The `simple_key` must be the same for both hiding and extracting the message.
- The image size limits the length of the hidden message. If the message is too long, it will raise an error.
- For security, in a real-world application, use a random salt for the key derivation function.


Here is a detailed explanation of how the **Hide and Extract Messages in Images** project works.

### **Overview**
The project uses a combination of cryptography and steganography to securely hide an encrypted message inside an image. The two main components of the project are:
- **Encryption:** Uses the Fernet encryption scheme, which is part of the `cryptography` library, to securely encrypt and decrypt the message.
- **Steganography:** Embeds the encrypted message into the pixels of an image, a process known as Least Significant Bit (LSB) steganography, allowing the message to be hidden without visibly altering the image.

The project consists of two Python scripts:
1. `hide.py`: Encrypts a message and hides it inside an image.
2. `show.py`: Extracts the hidden message from the image and decrypts it.

### **Part 1: Encrypting and Hiding a Message**

#### **1. Encrypting the Message**
Encryption is handled by the **Fernet encryption scheme**. The encryption key is derived from a user-provided passphrase (called `simple_key`), which is combined with a **key derivation function (KDF)**. The key steps are:

1. **Deriving the Key:**
   - The function `derive_key(simple_key)` derives a cryptographic key from the `simple_key` provided by the user. 
   - A static salt (in a real-world scenario, this should be randomized) is combined with the `simple_key`, and the **PBKDF2HMAC** (Password-Based Key Derivation Function) is used to create a 32-byte encryption key using the **SHA256** hashing algorithm.
   - This ensures that the same `simple_key` always generates the same encryption key, allowing the same key to be used for both encryption and decryption.

2. **Encrypting the Message:**
   - The function `encrypt_message(message, simple_key)` uses the derived key and encrypts the user-provided message using **Fernet encryption**.
   - The encrypted message is returned as a byte string, which will be hidden inside the image.

#### **2. Hiding the Message in the Image**
Once the message is encrypted, the next step is to hide it inside the pixels of an image.

1. **Loading the Image:**
   - The image is loaded using the **Pillow (PIL)** library, which allows for easy manipulation of images.
   - The image is converted to the **PNG** format to ensure lossless compression, which is important because lossy compression (like JPEG) can destroy hidden data.

2. **Converting the Image to an Array:**
   - The image is converted into a **NumPy array**, representing each pixel's RGB values. The RGB values of each pixel are stored as integers between 0 and 255.
   - The image is "flattened" into a one-dimensional array, making it easier to modify individual pixel values.

3. **Converting the Message to Binary:**
   - The encrypted message is converted into its binary representation (a string of `0`s and `1`s), which can be embedded into the image.
   - To ensure the message can be retrieved later, the **length** of the message in binary is also stored in the image.

4. **Least Significant Bit (LSB) Steganography:**
   - The core technique used to hide the message is **LSB steganography**. In this technique, the **least significant bit** (the rightmost bit) of each color component (R, G, or B) in the image is replaced with the bits of the encrypted message.
   - Since the least significant bit has the smallest impact on the overall color value, changing it does not create a noticeable visual difference in the image.
   - The first 32 bits of the image store the length of the hidden message, and the remaining bits store the binary message itself.

5. **Saving the Modified Image:**
   - After embedding the message, the modified NumPy array is converted back into a **PIL Image** and saved as a PNG file.
   - The result is an image that looks the same as the original but contains an encrypted, hidden message.

### **Part 2: Extracting and Decrypting the Message**

#### **1. Extracting the Message**
The `show.py` script extracts the hidden message from the image, following the reverse process.

1. **Loading the Image:**
   - The image is opened using the **Pillow** library and converted back into a NumPy array.

2. **Reading the Message Length:**
   - The first 32 pixels of the image store the binary representation of the message length (in bits). By reading the least significant bits of these pixels, we reconstruct the original message length.

3. **Extracting the Hidden Message:**
   - Once the length of the message is known, the script reads the next `n` bits (where `n` is the message length) from the least significant bits of the pixel values, reconstructing the binary message.

4. **Converting Binary to Bytes:**
   - The binary string is then divided into 8-bit chunks (each chunk representing one byte), which are converted back into a byte string, representing the encrypted message.

#### **2. Decrypting the Message**
Once the encrypted message is extracted, it needs to be decrypted to reveal the original hidden text.

1. **Deriving the Key:**
   - The same key derivation process (`derive_key`) is used to generate the encryption key from the `simple_key`.

2. **Decrypting the Message:**
   - The extracted message is decrypted using **Fernet decryption** with the derived key, revealing the original plaintext message.

### **Key Concepts**

- **Fernet Encryption:**
  - **Fernet** is a symmetric encryption algorithm that ensures the message is both encrypted and tamper-proof. It uses a randomly generated key and provides a secure method of hiding sensitive information.
  
- **PBKDF2HMAC Key Derivation:**
  - **PBKDF2HMAC** (Password-Based Key Derivation Function) combines a passphrase (simple_key) with a salt and applies many iterations of the **SHA256** hashing algorithm. This ensures that the key is secure and not easily guessable, even if the passphrase is simple.

- **LSB Steganography:**
  - **LSB steganography** is a technique where the least significant bit of the color values in an image is altered to encode a hidden message. This is useful because it doesn't significantly alter the appearance of the image, and only someone who knows the extraction technique can retrieve the hidden message.

### **Important Considerations**
- **Message Size:** 
  - The length of the hidden message is limited by the size of the image. Since only one bit per color component (3 bits per pixel) can be used to store the message, a very small image can only hide a short message.
  
- **Security:**
  - While the project demonstrates encryption and steganography, in a production environment, additional security measures would be necessary, such as using a random salt for the key derivation function and securely managing encryption keys.

- **Image Format:**
  - The project saves images in **PNG** format because it uses **lossless compression**. Using a lossy format like JPEG would destroy the hidden data.

### **Conclusion**
This project demonstrates a simple and effective way to hide and extract encrypted messages in images using a combination of cryptography and steganography. By utilizing these techniques, sensitive information can be concealed in plain sight, making it useful for applications where secure communication is needed.


## License
MIT License
```

This README should guide users on how to run the scripts and understand the purpose of each part of the project.
