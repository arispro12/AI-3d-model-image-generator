import base64
import os
import tkinter.messagebox
#VeRy LeGiT ImAgE gEnErAtOr
from tkinter import *
from tkinter import ttk
import openai
from PIL import Image,ImageTk
OUTPUT_DIR= "outputs"
client = openai.OpenAI(api_key = 'API KEY HERE')
from ttkthemes import ThemedTk
window = ThemedTk(theme="equilux")
window.configure(themebg="equilux")
window.geometry("1200x1200")
window.title("PolyGenix")
window.resizable(False, False)
ImagePreview = None


def generate_ideas(user_text,n):
    prompt = f"give me {n} creative 3D printable model ideas about :{user_text}\n" \
            f"Return ONLY {n} lines. No numbering, No bullets"

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    ideas = []
    for line in resp.choices[0].message.content.splitlines():
        tkinter.messagebox.showinfo("info!", line)
        line = line.strip()
        if line !="":
            ideas.append(line)
    return ideas[:n]

def generate_images_from_ideas2(ideas,):
    paths = []

    for i in range(len(ideas)):
        idea = ideas[i]

        img = client.images.generate(
            model="gpt-image-1.5",
            prompt=ideas[i],
            size="1024x1024",
            n=1,
            output_format="jpeg"
        )
        filepath = os.path.join(OUTPUT_DIR,f"request_{i+1}.jpg")
        b64 = img.data[0].b64_json
        print(b64)

        with open(filepath,"wb") as f:
            f.write(base64.b64decode(b64))
        paths.append(filepath)
    return paths


def generate_images_from_ideas(ideas):
    paths = []

    for i in range(len(ideas)):
        idea = ideas[i]

        img = client.images.generate(
            model="dall-e-3",
            prompt=idea,
            size="1024x1024",
            n=1
        )

        url = img.data[0].url
        print(url)

def preview():
    os.startfile(image_paths[0])


def showimage(ind):

    img=Image.open(image_paths[ind])
    print(image_paths[ind])
    print("test")
    img = img.resize((400,400),Image.Resampling.LANCZOS)
    imagePreview = ImageTk.PhotoImage(img)
    image_label.configure(image = imagePreview)
    image_label.image=imagePreview
    print("test")
def process(event=None):
    global image_paths
    user= text_widget.get()
    if rb.get() == "choice15":
        n=2
    else:
        n=1
    ideas = generate_ideas(user,n)
    image_paths = generate_images_from_ideas2(ideas)
    index = 0
    showimage(0)
#------------UI------------#
title = ttk.Label(window,text="PolyGenix", font=("Agency FB Bold",35))
title.place(x=500,y=30)
subtitle = ttk.Label(
    window,
    text="Idea Generation Engine for 3D Printable Designs",
    font=("Agency FB",15)
)
subtitle.place(x=400, y=89)
rb = StringVar(value="choice5")
rad1 = ttk.Radiobutton(window,text="Short (5 Variants)",value="choice5",variable=rb)
rad1.place(x=0,y=135)
rad2 = ttk.Radiobutton(window,text="Extended (15 Variants)", value="choice15", variable=rb)
rad2.place(x=850,y=135)
text_widget= ttk.Entry(window,width=100,font=("Segoe UI",15))
text_widget.place(x=50,y=200)
enter_button = ttk.Button(window, text="Enter",command=process)
enter_button.place(x=900,y=290,height=40,width=140)
preview_button = ttk.Button(window, text="Preview",command=preview)
preview_button.place(x=50,y=290,height=40,width=140)
image_label = ttk.Label(window,text="test")
image_label.place(x=400,y=300)
window.mainloop()


