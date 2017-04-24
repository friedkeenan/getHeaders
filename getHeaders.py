from requests import get
from os import makedirs,path,listdir
from shutil import rmtree
response=get("http://developer.limneos.net/index.php?ios=9.3.3").text
lines=response.split("\n")[128].split("</div>")[:-2]
unpause=False;
if not path.exists("Headers"):
    makedirs("Headers")
else:
    unpause=True
links=[]
for f in lines:
    f=f.split("<a href=")[1]
    f=f.split("'")[1]
    links.append(f)
if unpause:
    soFar=listdir("Headers")
    n=0
for f in links:
    d=f.split("framework=")[1][:-10]
    r=get("http://developer.limneos.net/index.php"+f).text
    lines=r.split("\n")[149].split("</div>")[2:-1]
    if d=="S":
        d="SpringBoard"
    if unpause:
        d2=links[links.index(f)+1].split("framework=")[1][:-10]
        if d2 in soFar:
            print("Skipped "+d)
            continue
        else:
            soFar=listdir("Headers\\"+d)
            for j in lines:
                try:
                    soFar[n]
                    n+=1
                except IndexError:
                    lines=lines[n:]
                    unpause=False
                    break
    if not path.exists("Headers\\"+d):
        makedirs("Headers\\"+d)
    for h in lines:
        if h:
            htmp=h
            h=h.split("<a href=")
            if len(h)==1:
                break
            h=h[1]
            h=h.split("'")[1]
            i=get("http://developer.limneos.net/index.php"+h).text
            lines2=i.split("\n")[130].split("</div>")
            lines2=lines2[1].split("<a href=")[1].split("'")[1]
            h=lines2.split("Headers/")[1]
            i=get(lines2)
            with open("Headers\\"+d+"\\"+h,"wb") as head:
                head.write(i.content)
            print("Downloaded "+str(lines.index(htmp)+1+n)+"/"+str(len(lines)+n)+" from "+d+": "+h)
    n=0
