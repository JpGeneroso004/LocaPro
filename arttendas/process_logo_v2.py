from PIL import Image

def process_logo_v2():
    path = r'C:\ArtTendas\arttendas\static\img\logo.png'
    img = Image.open(path).convert('RGBA')
    
    data = img.getdata()
    new_data = []
    
    for item in data:
        r, g, b, a = item
        
        if a == 0:
            new_data.append(item)
            continue
            
        # condition for white/light text: convert to dark gray
        if r > 180 and g > 180 and b > 180:
            new_data.append((50, 50, 50, a))
            
        # condition for yellow/gold tent
        # yellow has high red and green, low blue.
        elif r > 80 and g > 60 and (r > b + 20) and (g > b + 20):
            # keep it, it's part of the tent
            new_data.append(item)
            
        # everything else (shadows, dark grays, dark backgrounds) becomes transparent
        else:
            new_data.append((255, 255, 255, 0))
            
    img.putdata(new_data)
    img.save(r'C:\ArtTendas\arttendas\static\img\logo_contrato.png')
    print("Refined logo saved successfully.")

if __name__ == "__main__":
    process_logo_v2()
