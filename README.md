Here is a **README** in markdown format for your project:

```markdown
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

## License
MIT License
```

This README should guide users on how to run the scripts and understand the purpose of each part of the project.
