from tkinter import *
import os
from tkinter import scrolledtext
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfilename, askopenfilename
layers=[]
ss=[]
r=Tk()
r.title('svg animation')
r.geometry('600x650')
Label(r,text='Enter your SVG:').grid(column=0,row=0)
def click():
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
    r.iconbitmap('icon.ico')
except:
    pass
r.mainloop()