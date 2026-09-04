from PIL import Image

def process_logo():
    path = r'C:\ArtTendas\arttendas\static\img\logo.png'
    img = Image.open(path).convert('RGBA')
    
    data = img.getdata()
    new_data = []
    
    for item in data:
        r, g, b, a = item
        # If dark/black pixel, make transparent
        if r < 40 and g < 40 and b < 40:
            new_data.append((255, 255, 255, 0))
        # If white/light pixel, make black
        elif r > 200 and g > 200 and b > 200:
            new_data.append((17, 17, 17, a))
        else:
            # Keep yellow or other colors
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(r'C:\ArtTendas\arttendas\static\img\logo_contrato.png')
    print("Logo saved successfully.")

if __name__ == "__main__":
    process_logo()
