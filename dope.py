import numpy as np
import sys
import random


if len(sys.argv)!=4:
   print("Please enter: \n ""python dope.py input_file dosage Dopping atom" )
   print("Example: ""python dope.py Fe3O4_r11.xyz 25 Cu")
   quit() 


filename = sys.argv[1]
dope_percentage = float(sys.argv[2])
doping_element = sys.argv[3]
f = open(str(filename), "r")

filename_doped=filename[:-4]+"_doped_"+doping_element+"_"+str(dope_percentage)[0:2]+"_percent.xyz"

f2 = open("new_geometry1.xyz","w+")
f3 = open(filename_doped,"w+")


f1 = f.readlines()[2:]

atom,x,y,z,r, r_list= [], [], [], [], [], []
n_fe=0
n_o=0
n_fe_on_surface=0


for l in f1:
    row = l.split()
    xx=float(row[1])
    yy=float(row[2])
    zz=float(row[3])
    rr=(xx**2+yy**2+zz**2)**0.5  
    r_list.append(rr)

r_particle=max(r_list)
print('r_particle=',r_particle)    



for l in f1:
    row = l.split()
    atomm=row[0]
    atom.append(atomm)
    if atomm=='Fe':
       n_fe=n_fe+1
    if atomm=='O' :
       n_o=n_o+1
       
    xx=float(row[1])
    yy=float(row[2])
    zz=float(row[3])
    rr=(xx**2+yy**2+zz**2)**0.5
            
    x.append(xx)
    y.append(yy)
    z.append(zz)
    r.append(rr)
    
    if atomm=='Fe' and rr>(0.9*r_particle):
       n_fe_on_surface=n_fe_on_surface+1




#print(x[0:4])
n_atom=len(atom)
x_ave=np.average(x)
y_ave=np.average(y)
z_ave=np.average(z)
ind=np.argsort(r)

#print(x_ave,y_ave,z_ave)

f2.write(str(n_atom)+'\n')
f2.write("Sorted Fe3O4"+'\n')

for i in range(n_atom):
    new_x=x[ind[i]]
    new_y=y[ind[i]]
    new_z=z[ind[i]]
    f2.write(atom[ind[i]]+"\t"+str(new_x)+"\t"+str(new_y)+"\t"+str(new_z)+"\t"+str(r[ind[i]])+'\n')
f2.close()     
      
print('n_atom',n_atom)
print('n_fe=',n_fe)
print('n_o=',n_o)
print('n_fe_on_surface=',n_fe_on_surface)

n_doped = round(dope_percentage*n_fe_on_surface/100)
print('n_doped',n_doped)      

 
 
f2 = open("new_geometry1.xyz","rt")
f4 = open(filename_doped,"wt")
n_doping_element=0


lines=f2.readlines()[2:]
new_line = [None] * len(lines);    

for i in range(0, len(lines)):    
   new_line[i]=lines[i]



while n_doping_element<n_doped:
  rand_index=random.randint(1,n_atom-1)
  row=lines[rand_index].split()
  atomm=row[0]
  rr=float(row[4])
  if atomm=='Fe' and rr>(0.9*r_particle) and n_doping_element<n_doped:
     new_line[rand_index]=lines[rand_index].replace('Fe',doping_element)
     n_doping_element=n_doping_element+1



f4 = open(filename_doped,"w+")
f4.write(str(n_atom)+'\n')
f4.write("Doped Fe3O4"+'\n')

for item in new_line:
    row=item.split()
    atomm=row[0]
    x=row[1]
    y=row[2]
    z=row[3]
    f4.write(atomm+"\t"+str(x)+"\t"+str(y)+"\t"+str(z)+"\t"+'\n')


f2.close()
f4.close()

print("****************** Doping finished successfully *********************")
print("New file:  ", filename_doped )

