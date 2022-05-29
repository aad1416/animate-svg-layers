from tkinter import *
from tkinter import scrolledtext
layers=[]
ss=[]
r=Tk()
r.title('svg animation')
r.geometry('600x650')
Label(r,text='Enter your SVG:').grid(column=0,row=0)
def click():
    outputtext['state']='normal'
    outputtext.delete(0.0,END)
    inpsvg=inputsvg.get(0.0,END)
    inpsvg=inpsvg.replace('\n','').replace('\t','').replace('  ',' ').replace("'",'"')
    for i in inpsvg.split('<g id="')[1:]:
        ss.append('l'+str(inpsvg.split('<g id="').index(i))+i[i.find('"'):])
        layers.append(i[:i.find('"')])
    style="<style>.layer{opacity:0}</style>"
    modif=f'''{inpsvg.split('<g id="')[0]}{style}<g class="layer" id="{'<g class="layer" id="'.join(ss)}'''
    num = len(layers)
    time=str(num*100)
    script=f'''<script>var l=document.querySelectorAll(".layer");i=0;l[0].style.opacity="1";setInterval(function(){{if(i>l.length-1){{i=-1}}else if(i==0){{try{{l[l.length-1].style.opacity="0"}}catch{{}};l[i].style.opacity="1"}}else{{l[i-1].style.opacity="0";l[i].style.opacity="1";}};i++;}},{time})</script>'''
    #scriptdis=f'''<script>var l=document.querySelectorAll(".layer");i=0;setInterval(function(){{if(i>l.length-1){{i=-1}}else if(i==0){{try{{l[l.length-1].style.display="none"}}catch{{}};l[i].style.display="block"}}else{{l[i-1].style.display="none";l[i].style.display="block";}};i++;}},{time})</script>'''
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
    outsvg=outputtext.get(0.0,END)
    r.clipboard_append(outsvg)
    r.update()
outputtext = Text(r, width=scrol_w, height=scrol_h)
outputtext.grid(column=1,row=3)
b=Button(r,text='convert',width=20,height=3,command=click)
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



