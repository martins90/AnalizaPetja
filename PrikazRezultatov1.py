import matplotlib.pyplot as plt
import numpy as np
import os.path
import math as math

# branje rezultatov iz sonic visualizerja

mediane = {}
mediane_intervali = {}
podatki_za_izris = []
podatki_za_izris_intervali =[]

zacetki = []

note = []
f = open("midi.txt", "rt") # midi - zakrivljeno, midi1 - tam dol na ravnem polju
note_podatki = f.readline().strip().split(",")
for x in range(len(note_podatki)):
    note.append(float(note_podatki[x]))
    mediane[x] = []

all = []
n = 0
kandidati = 0


for fname in os.listdir("./rezultati_1/"):
    if fname[:3] == "zak": # zak - zakrivljeno, tam - tam dol na ravnem polju
        #fname = ""
        f = open("./rezultati_1/"+fname, "rt")
        midiji = []
        for vrstica in f:
            midiji.append(vrstica.split(",")[1])

        prejsnja = 69 + 12 * math.log((1.0 * float(midiji[0]) / 440), 2)

        #absolutna razlika
        xs = []
        xs.append(float("{0:.4f}".format(prejsnja)))

        for x in range(1, len(note)):
            xs.append(xs[x-1] + note[x])

        for i in range(0, len(midiji)):
            trenutna = float("{0:.4f}".format(69 + 12 * math.log((1.0 * float(midiji[i]) / 440), 2)))
            #print trenutna, " - ", note[i], " ", xs[i]," = ", trenutna - xs[i]
            x = trenutna - xs[i]
            if x < 1.5 and x > -1.5:
                mediane[i].append(x) #float("{0:.4f}".format(x)))
                kandidati += x
                n += 1
                all.append(x)


mediana_sproti = [0]
mediana = [0, 0]
for i in range(1, len(mediane)):
    x = np.median(np.array(mediane[i]))
    mediana_sproti.append(x)
    mediana.append(np.median(np.array(mediana_sproti)))

print len(mediana_sproti)
print len(mediana)
print len(mediane)


print " skupni premik mediana" ,np.median(np.array(all))
print " skupni premik avg , ", kandidati/n

# kopiranje podatkov v seznam za izris na grafu
for m in range(len(mediane)):
    podatki_za_izris.append(mediane[m]) # za izpis not
    #print m , " ", mediane[m]
    #podatki_za_izris_intervali.append(mediane_intervali[str(m)]) # za izpis koliko je zgreseno


plt.figure(1)
plt.plot(mediana, label='Mediana', color='y')
plt.boxplot(podatki_za_izris) #, showfliers=False, label='')

xos= np.arange(1, len(note_podatki)+1)

plt.xticks(xos, note_podatki)
plt.axvline(1.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(4.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(7.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(9, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(10.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(13.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(16.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(17, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(18.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(21.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(24.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(26, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(27.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(30.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(33.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija

plt.axhline(0, color='k', linestyle='--', alpha=0.3)  #vertikalna linija
'''
plt.axvline(2.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(4.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(6.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(8.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(10.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(13.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(16, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(16.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(18, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(20.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(22.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(24.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(26, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
plt.axvline(28.5, color='k', linestyle='--', alpha=0.2)  #vertikalna linija
'''
plt.xlabel('Intervali')
plt.ylabel('Odstopanje v poltonih')
plt.title('Veseli pastir')
#plt.savefig("NaPlanincah_note.png")
plt.legend()

plt.show()