from PIL import Image

class steg:
    def __init__(self, image_path):
        self.img = Image.open(image_path)
        self.pixels = self.img.load()
        
    def encode(self, secret, output_path):
        secret_bin = ''.join(format(ord(c), '08b') for c in secret)
    
        secret_len = len(secret_bin)
        secret_len_bin = format(secret_len, '08b')
        
        if self.img.height * self.img.width * 3 < secret_len + 8:
            print("Image too small to hide the message")
        
        self.encode_sub(secret_len_bin, isMessage=False)
        self.encode_sub(secret_bin, isMessage=True)
    
        self.img.save(output_path, "PNG")
        print(f"secret encoded and saved to {output_path}")
 
    def encode_sub(self, binary, isMessage):        
        length = len(binary)
        msg_index = 0
        startPt = 8 if isMessage else 0
        
        for x in range(self.img.height):
            for y in range(self.img.width):
                if msg_index >= length:
                    return 
                
                if startPt >= 0:
                    startPt -= 1
                    continue
                
                r, g, b = self.pixels[x, y]
                
                if msg_index < length:
                    # 0xFE is 254 or 1111 1110, thus performing 'and' op. with it makes the LSB 0
                    # and then performing 'or' op. with the bit to be encoded changes the LSB
                    r = (r & 0xFE) | int(binary[msg_index])
                    msg_index += 1
                if msg_index < length:
                    g = (g & 0xFE) | int(binary[msg_index])
                    msg_index += 1
                if msg_index < length:
                    b = (b & 0xFE) | int(binary[msg_index])
                    msg_index += 1
                
                self.pixels[x, y] = (r, g, b)
    
    def decode(self):
        message_len_bin = self.decode_sub(8, isMessage=False)
        message_len = int(message_len_bin, 2)
        
        secret_bin = self.decode_sub(message_len, isMessage=True)
        secret = ''.join(
            chr(int(secret_bin[i:i+8], 2)) for i in range(0, len(secret_bin), 8)
        )
        
        return secret
     
    def decode_sub(self, length, isMessage):
        binary = ""
        msg_index = 0
        startPt = 8 if isMessage else 0
        
        for x in range(self.img.height):
            if msg_index >= length:
                    break
            for y in range(self.img.width):
                if msg_index >= length:
                    break
                
                if startPt >= 0:
                    startPt -= 1
                    continue
                
                r, g, b = self.pixels[x, y]
                
                if msg_index < length:
                    binary += str(r & 1)  
                    msg_index += 1
                if msg_index < length:
                    binary += str(g & 1) 
                    msg_index += 1
                if msg_index < length:
                    binary += str(b & 1) 
                    msg_index += 1
                    
        return binary

img = steg('./kat03.png')
img.encode("hello there", "./output.png")
print(img.decode())