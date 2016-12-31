import numpy as np
import matplotlib.pyplot as plt
import os.path

medianeS = []
medianeA = []
medianeT = []
medianeB = []

noteS = [67,69,71,73,75,77,79]
noteA = [60,62,64,66,68,70,72]
noteT = [52,53,54,55,56,57,58,59,60,61,62,63,64]
noteB = [48,41,50,43,52,45,54,47,56,49,58,51,60]
podatki_za_izris = []
podatki_za_izris1 = []

f = open("./rezultati_1/MEDIANE.txt", "rt")
note_podatki = f.readline().strip().split(";")
for i in range(1,len(note_podatki)-1):
	medianeS.append(float(note_podatki[i]))
	
note_podatki = f.readline().strip().split(";")
for i in range(1,len(note_podatki)-1):
	medianeA.append(float(note_podatki[i]))
	
note_podatki = f.readline().strip().split(";")
for i in range(1,len(note_podatki)-1):
	medianeT.append(float(note_podatki[i]))
	
note_podatki = f.readline().strip().split(";")
for i in range(1,len(note_podatki)-1):
	medianeB.append(float(note_podatki[i]))
	
#izracun zgresitve
for i in range(len(noteS)):
    medianeS[i] = float("{0:.2f}".format(medianeS[i] - noteS[i]))
    medianeA[i] = float("{0:.2f}".format(medianeA[i] - noteA[i]))
for i in range(len(noteT)):
    medianeT[i] = float("{0:.2f}".format(medianeT[i]-noteT[i]))
    medianeB[i] = float("{0:.2f}".format(medianeB[i] - noteB[i]))

# razdelitev not soprana in alta na dvoje, tiste ki so povezane
for i in range(0, len(noteT)-1, 2):
    medianeA.insert(i+1, medianeA[i])
    medianeS.insert(i + 1, medianeS[i])

medianeA.insert(0, None)
medianeS.insert(0, None)
medianeT.insert(0, None)
medianeB.insert(0, None)

xos = [1,2,3,4,5,6,7,8,9,10,11,12,13]
plt.figure(1)
plt.plot(medianeS, linestyle='--', marker='v', label="Sopran")
plt.plot(medianeA, linestyle='--', marker='o', label="Alt")
plt.plot(medianeT, linestyle='--', marker='D', label="Tenor")
plt.plot(medianeB, linestyle='--', marker='s', label="Bas")
plt.xticks(xos)
plt.axhline(0, color='k', linestyle='-', alpha=0.3)  #hor linija
plt.axvline(2.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(4.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(6.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(8.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(10.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(12.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.xlabel('Stevilka note')
plt.title('Napaka pri petju')
plt.ylabel('Napaka v poltonih')
plt.legend()

plt.show()