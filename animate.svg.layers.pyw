from tkinter import *
import os,base64
from tkinter import scrolledtext
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfilename, askopenfilename
r=Tk()
r.title('svg animation')
r.geometry('600x650')
Label(r,text='Enter your SVG:').grid(column=0,row=0)
def click():
    layers=[]
    ss=[]
    outputtext['state']='normal'
    outputtext.delete(1.0,END)
    inpsvg=inputsvg.get(1.0,END)
    inpsvg=inpsvg.replace('\n','').replace('\t','').replace('  ',' ').replace("'",'"')
    for i in inpsvg.split('<g id="')[1:]:
        ss.append('l'+str(inpsvg.split('<g id="').index(i))+i[i.find('"'):])
        layers.append(i[:i.find('"')])
    style="<style>.layer{opacity:0}</style>"
    modif=f'''{inpsvg.split('<g id="')[0]}{style}<g class="layer" id="{'<g class="layer" id="'.join(ss)}'''
    num = len(layers)
    time=str(num*70)
    script=f'''<script>var l=document.querySelectorAll(".layer");i=1;l[0].style.opacity="1";setInterval(function(){{if(i>l.length-1){{i=0}};if(i==0){{l[l.length-1].style.opacity="0";l[i].style.opacity="1"}}else{{l[i-1].style.opacity="0";l[i].style.opacity="1";}};i++;}},{time})</script>'''
    #scriptdis=f'''<script>var l=document.querySelectorAll(".layer");i=1;setInterval(function(){{if(i>l.length-1){{i=0}}; if(i==0){{l[l.length-1].style.display="none";l[i].style.display="block"}}else{{l[i-1].style.display="none";l[i].style.display="block";}};i++;}},{time})</script>'''
    if len(inpsvg.split('<g id="'))>1:
        output=f'''{script}</svg>'''.join(modif.split('</svg>'))
        #outputdis=f'''{scriptdis}</svg>'''.join(modif.split('</svg>'))
    else:
        output='input not in a correct format'
    outputtext.insert(END, output)
    outputtext['state']='disable'
scrol_w = 60
scrol_h = 15
inputsvg = Text(r, width=scrol_w, height=scrol_h)
inputsvg.grid(column=1,row=1)
def copy():
    outsvg=outputtext.get(1.0,END)
    r.clipboard_append(outsvg)
    r.update()
def quit_application():
        r.destroy()

def show_about():
	showinfo("animate SVG layers", "github:@aad1416/animate-svg-with-layers")

def open_file():
	file_name = askopenfilename(
		defaultextension=".svg",
		filetypes=[("SVG", "*.svg") , ("All Files", "*.*")])

	if file_name == "":
		file_name = None

	else:
		r.title(os.path.basename(file_name) + " - svg animation")
		inputsvg.delete(1.0, END)

		with open(file_name, 'r') as file:
			inputsvg.insert(1.0, file.read())

def new_file():
	r.title("svg animation")
	inputsvg.delete(1.0, END)

def save_file():
    file_name = asksaveasfilename(
        initialfile='Untitled.svg', defaultextension=".svg",
        filetypes=[("SVG", "*.svg") , ("All Files", "*.*")])

    if file_name == "":
        file_name = 'Untitled.svg'

    else:
        with open(file_name, 'w') as file:
            file.write(outputtext.get(1.0, END))

        r.title(os.path.basename(file_name) + " - svg animation")
menu_bar = Menu(r)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_application)
menu_bar.add_cascade(label="File", menu=file_menu)
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="about", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
r.config(menu=menu_bar)
outputtext = Text(r, width=scrol_w, height=scrol_h)
outputtext.grid(column=1,row=3)
b=Button(r,text='animate SVG',width=20,height=3,command=click)
b.grid(column=1,row=2)
c=Button(r,text='copy output',width=20,height=3,command=copy)
c.grid(column=1,row=4)
try:
    svgcode=r.clipboard_get()
    inputsvg.insert(END, svgcode)
except:
    pass
try:
    icondata= base64.b64decode('AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAP1rAAD9awAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABoaGgAaGhoAGg0KABoQDgEaKi4EHoqdAR15igAUFxoAEAAAAA0AAAMUAAANFAAADQ0AAAMRAAAAFBcaAB17jQAejKABGiouBBoQDgEaDQoAGhoaABoaGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaGhoAGQAAABgAAAAaISMDGiwxARYEBwAVBggJGQAARxoWFosbNTy8G0lU1xxUYeMcVGHjG0pV1xs2PLwaFxaMGQAARxYGCAkWBAcAGiwxARohIwMYAAAAGQAAABoaGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZGRkAGhoaABoWFQAaFhUBGhobAxcAAAAXAAAPGQsKextETeMdfZT/HqrL/h/F7f8f0/3/H9n//x/Y//8f0/3/H8Xt/x6qy/4dfZT/G0RO5BkLCnsXAAAPFwAAABoaGwMaFhUBGhYVABoaGgAZGRkAAAAAAAAAAAAAAAAAGBgYABoaGgAaGRkAGhUVARsgIAMaAAAAGQAAUhs+RuUdlbL/H9T7/h/k//0f3v/7H9j//B/T/v0f0fz+H9H8/h/T/v0f1//8H97/+x/k//0f1Pv+HZWz/xs+RuYZAABSGgAAABsgIAMaFRUBGhkZABoaGgAYGBgAAAAAAAAAAAAaGhoAGhkZABkLCgEdYWgCKf//ABoODY4can7/H9P4/h/j//sf1P79H9D6/x/Q+v8f1f7/H9z//x/f//8f3///H9z//x/V/v8f0Pr/H9D6/x/U/v0f4//7H9P4/hxrfv8aDw2OKv//AB1iaQIZCwoBGhkZABoaGgAAAAAAGhoaABoaGgAZAAAAHYGOAiT//wAaExKhHYeg/yDn//of1vz9H9H8/x/S/f8f2P7/H+P//x/O9v8esdX/HqLB/x6iwf8esdT/H872/x/j//8f2P7/H9L9/x/R/P8f1vz9IOf/+h2Hof8aExOhJf//AB2CjwIZAAAAGhoaABoaGgAaGhoAFgAAABs3PAMaDAkAGgkHjR2IoP8g6P/6H9D6/x/T/v8f0v7/H9z//x/I6v8ccIX/HFhm/xxmeP8ccof/HHKH/xxmeP8cWGb/HG+E/x/I6v8f3P//H9L+/x/T/v8f0Pr/IOj/+h2IoP8aCQeNGgwJABs3PAMRAAAAGhoaABcAAAAaEQ8DGAAAABkAAFYcbX7/H+b/+x/Q+/8f1P//H9P9/x/a//8eu93/G0pV/x2QrP8fz/j/H9///x/i//8f4v//H9///x/Q+f8dkq3/G0pV/x662/8f2v//H9P9/x/U//8f0Pv/H+b/+xxtfv8ZAABWGAAAABoRDwMXAAAAGhYVARYAAAAXAAARGz5H4B/T9f8f1f/9H9P+/x/U//8f0/3/H9z//xxXZ/8eqsb/IOr//x/U/f8f0vz/H9H7/x/R+/8f0vz/H9T9/yDq//8eq8f/HFdm/x/c//8f0/3/H9T//x/T/v8f1f/9H9P1/xs+RuAXAAARFgAAABoWFQEaICEEGQAAABkHBHwdl6//H+P/+x/R/P8f1P//H9T//x/U//8f0v7/Hrna/x/Y/f8f0f3/H9T//x/U//8f1P//H9T//x/U//8f1P//H9H9/x/Y/f8eudr/H9L+/x/U//8f1P//H9T//x/R/P8f4//7HZev/xkHBHwZAAAAGiAhBBUAAAAUAAAKG0VO3h/U+f8f1P/9H9T//x/U//8f1P//H9T//x/U//8f2v7/H9P+/x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9P+/x/a/v8f1P//H9T//x/U//8f1P//H9T//x/U//0f1Pn/G0VO3hQAAAoVAAAAGQAAABkAAEgdf5P/H+P//R/R/P8f1P//H9T//x/U//8f1P//H9T//x/T/f8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9P9/x/U//8f1P//H9T//x/U//8f1P//H9H8/x/j//0df5L/GQAASBkAAAAaGRkAGhcWih6qyP8f3v/7H9L9/x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f1P//H9T//x/U//8f0v3/H97/+x6qyP8aFxaKGhkYAB6hugAbNju6H8Xr/x/Y//wf0/7/H9T//x/U//8f1P//H9P9/x/S/P8g0/7/H9H8/x/T/v8f1P//H9T//x/U//8f1P//H9T//x/U//8f0/7/H9H8/yDT/v8f0vz/H9P9/x/U//8f1P//H9T//x/T/v8f2P/8H8Xr/xs2O7oenrYABAAAAxtKVNYf0/3/H9T//R/U//8f1P//H9T//x/S/v8h2/7/IOH//xvZ//8h4v//Idn+/x/S/v8f1P//H9T//x/U//8f1P//H9L+/yHY/v8g4v//G9n//yDh//8h2/7/H9L+/x/U//8f1P//H9T//x/U//0f0/3/G0pT1gMAAAMUAAAMHFRh4x/Y//8f0/7+H9T//x/U//8f0v3/Id7//xe42v8ZY3b/K1pl/xZpfv8ZxOb/Idv//x/S/v8f1P//H9T//x/S/v8h2///Gcbo/xduhP8uYGv/Gmd6/xe52/8h3f//H9L9/x/U//8f1P//H9P+/h/Y//8cVGHjFAAADBQAAAwcVGHjH9j//x/T/v4f1P//H9L9/yHc//8WsdL/OkRG/7qoof/azsr/r5uV/y5HTf8Zw+f/Idn//x/T/v8f0/7/Idn//xnE6P8uSlD/sJuV/9zQy//Araf/P0tO/xaz1f8h3P//H9L9/x/U//8f0/7+H9j//xxUYeMUAAAMBAAAAxtKVNYf0/3/H9T//R/U//8g0/7/Hdr//yJTXf/XyMT//////+rp5//4+vj/tKCa/xdgcP8g4f//H9L8/x/S/P8g4f//GWR1/8Ctqf//////6uro//T18//Pvbj/I1di/x3b//8g0/7/H9T//x/U//0f0/3/G0pT1gMAAAMeoroAGzY7uh/F6/8f2P/8H9L9/yLc//8QsNb/ZWlq///////8/f3//f39//Hw7//x6eX/RVdb/xbF7/8h1///Idf//xTF7/9NYmb////9//v8/f//////7+7t//Lt6f9jZ2f/EbPa/yLc//8f0v3/H9j//B/F6/8bNju6Hp62ABoZGQAaFxeKHqrJ/x/e//sf0fv/I+D//w6dv/+Cfn3///////////9jY2P/Dg8P/9fSz/9lamr/ELHY/yLb//8i2///DbHX/3d/gf+mpKP/AAAA/7S0tP//////9/Ty/314dv8PocT/I9///x/R+/8f3v/7HqrI/xoXF4oaGRkAGQAAABkAAEgdf5P/H+P//R/Q+v8j3v//D6rP/25vb///////4eHh/ykpKf9OT0//j4qI/19sbv8RvOX/Idj//yLY//8Sv+j/Wmpu/2hk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')
    tempFile= "icon.ico"
    iconfile= open(tempFile,"wb")
    iconfile.write(icondata)
    iconfile.close()
    r.wm_iconbitmap(tempFile)
    os.remove(tempFile)
except:
    pass
r.mainloop()