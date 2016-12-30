import os.path
import sys
import math as math
import scipy as sp
from scipy import signal
from scikits.audiolab import wavread
import numpy as np

import matplotlib.pyplot as plt

medianeS = []
medianeA = []
medianeT = []
medianeB = []

noteS = []
noteA = []
noteT = []
noteB = []
podatki_za_izris = []
podatki_za_izris1 = []


w=2205
hamwindow=[None]*w
for n in range(0,w):
    hamwindow[n] = 0.53836 - 0.46164 * math.cos((2*math.pi*n)/(w-1))

def butter_lowpass(cutoff, sr, order=5):
    nyq = 0.5 * sr
    normal_cutoff = cutoff / nyq
    b, a = sp.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, sr, order=5):
    b, a = butter_lowpass(cutoff, sr, order=order)
    y = sp.signal.lfilter(b, a, data)
    return y

def hamm_window(data):
    ham = []
    for i in range(len(data)):
        ham.append(data[i] * hamwindow[i])
    return ham

def autocorrelation(x):
    #hammingovo okno
    #x= hamm_window(x)

    # autocorrelation z FFT
    x = np.asarray(x)
    N = len(x)
    x = x - x.mean()
    s = np.fft.fft(x, N * 2 - 1)
    result = np.real(np.fft.ifft(s * np.conjugate(s), N * 2 - 1))
    result = result[:N]
    result /= result[0]
    return result

def estimate_period(x, n, minP, maxP):

    # x vzorci
    # n stevilo vzorcev
    # minP najmanjsa perioda ki nas zanima
    # maxP najvecja perida ki nas zanima
    # q kvaliteta; 1 = peridoicen signal

    if(minP < 1) or (maxP < minP) or (n < 2*maxP):
        return -1

    q = 0

    #Compute the normalized autocorrelation (NAC). The normalization is such that
    #if the signal is perfectly periodic with (integer) period p, the NAC will be
    #exactly 1.0.  (Bonus: NAC is also exactly 1.0 for periodic signal
    #with exponential decay or increase in magnitude).

    nac = [None] * (maxP+2) # do maxP+2 ker moramo preveriti tudi element maxP+1,
                            # da ugotovimo ce je mogoce maxP vrh

    nac = autocorrelation(x)

    # Find the highest peak in the range of interest.
    # Get the highest value

    bestP = minP
    for p in range(minP, maxP):
        if nac[p] > nac[bestP]:
            bestP = p

    # Give up if it's highest value, but not actually a peak.
    # This can happen if the period is outside the range [minP, maxP]
    if nac[bestP] < nac[bestP - 1] and nac[bestP] < nac[bestP + 1]:
        return 0.0

    # "Quality" of periodicity is the normalized autocorrelation
    # at the best period (which may be a multiple of the actual period

    q = nac[bestP]

    #Interpolate based on neighboring values
    #E.g. if value to right is bigger than value to the left,
    #real peak is a bit to the right of discretized peak.
    #if left  == right, real peak = mid;
    #if left  == mid,   real peak = mid-0.5
    #if right == mid,   real peak = mid+0.5

    mid = nac[bestP]
    left = nac[bestP - 1]
    right = nac[bestP + 1]

    if (2*mid - left - right) < 0:
        return -2

    shift = 0.5 * (right - left) / (2 * mid - left - right)
    #print " best = ", bestP , " vrednost " , nac[bestP]
    pEst = bestP + shift
    #print " pEst = ", pEst , " vrednost " , nac[pEst]

    #If the range of pitches being searched is greater than one octave, the basic algo above may make "octave"
    #errors, in which the period identified is actually some integer multiple of the real period.  (Makes sense, as
    #a signal that's periodic with period p is technically also period with period 2p).

    #Algorithm is pretty simple: we hypothesize that the real period is some "submultiple" of the "bestP" above.  To
    #check it, we see whether the NAC is strong at each of the hypothetical subpeak positions.  E.g. if we think the real
    #period is at 1/3 our initial estimate, we check whether the NAC is strong at 1/3 and 2/3 of the original period estimate.


    k_subMulThreshold = 0.90 #If strength at all submultiple of peak pos are
                             #this strong relative to the peak, assume the
                             #submultiple is the real period.

    return pEst

def clipping(data, cl=0.10):
    r = []
    for x in data:
        if abs(x) <= cl:
            x = 0
        elif x > cl:
            x = x-cl
        else:
            x = x+cl
        r.append(x)
    return r

def obdelaj_posnetek(posnetek, velikost_okna=50, min_frek=65.4, max_frek=1396.91, cutoff=400):

    # Branje posnetka
    filename = posnetek
    data,sample_rate,encoding = wavread(filename)

    #clipping
    #data = clipping(data, 0.10)

    # dolocanje dolzine okna v ms
    okno=velikost_okna #za 44100 vsaj 35

    frekvence=[0]
    note = [0]
    cas=[0]

    # import sounddevice as sd # predvajanje
    # sd.play(data, 44100)

    # pretvorba iz okna v ms v okno v vzorcih
    delcek=int(round(okno * sample_rate / 1000)) # za 50 = 2205, za 35 = 1543

    # prvi vzorec dolzine okna
    indata = data[0:delcek]
    i=delcek

    # dolocanje mej v Hz
    minF = min_frek #65.4 # Nizki C (C2)
    maxF = max_frek #1046.50 # Sopranski C (C6)
    # prezvorba mej v vzorce
    minP = int(round(sample_rate/maxF-1)) # Minimum period
    maxP = int(round(sample_rate/minF+1)) # Maximum period

    while len(indata) == delcek:
        # lowpass filter na oknu
        indata = butter_lowpass_filter(indata, cutoff, sample_rate, 5)

        pEst = estimate_period(indata, delcek, minP, maxP)
        nota = 0
        fEst = 0
        if pEst > 0:
            # izracun frekvence
            fEst = sample_rate / pEst
            # predvorba iz vrekvenc v "int" midi zapis note (69,70,...)
            nota = 69 + 12 * math.log((1.0 * fEst / 440), 2)
            nota = float("{0:.2f}".format(nota))
            fEst = float("{0:.2f}".format(fEst))
        frekvence.append(fEst)#nota)
        note.append(nota)
        cas.append(cas[-1] + delcek)

        # prebrano novo okno za naslednjo iteracijo
        indata = data[i:i + delcek]
        i += delcek

    return frekvence, note

def pobrisi(list, start, n, smer = 1):
    for i in range(start, start+n, smer):
        if list[i] == 0: # do prve pobrisi
            return list
        else:
            list[i] = 0

    return list

def je_zadnja(list, x):
    for i in range(4):
        if x+i < len(list):
            if list[x+i] == 0:
                return True
    return False

def je_prva(list, x):
    for i in range(x,x-4,-1):
        if list[i] == 0:
            return True
    return False

def filtriraj_rezultate(list, razlika):
    n = 0
    vrednosti = 0
    for x in range(len(list)):
        if list[x] != 0:
            if n == 0: # prvi v vrsti ki != 0
                n = 1
                vrednosti = list[x]
            else: # nekje vmes ki != 0

                # ce je vrednost prevelika/premajhna od ostalih
                if abs(list[x] - vrednosti/n) > razlika:

                    #pogledati ce je mogoce prejsnja vrednost v nizu tista ki izstopa in je od te vrednosti naprej lep niz
                    if je_prva(list, x) != 0:
                        list[x-1] = 0
                        n = 1
                        vrednosti = list[x]

                    #pogledati ce je mogoce to zadnja vrednost v nizu
                    elif je_zadnja(list, x):
                        list[x] = 0
                        n = 0
                        vrednosti = 0

                    else: # zamenjamo ga z 0
                        list[x] = 0
                        n = 0
                        vrednosti = 0
                # ce vrednost ustreza, gremo naprej
                else:
                    n += 1
                    vrednosti += list[x]

        else:#list[x] == 0
            if n != 0 and n <2: # ce je bilo uporabnega signala manj kot 200ms ga pobrisemo
                list = pobrisi(list, x-n, n)
            n = 0
            vrednosti = 0

    return list


def list_v_string(list):
    s = ""
    for vrednost in list:
        s += str(vrednost)+";"
    return s

def zdruzi_note(list):
    rezultat = []
    kandidati = []
    stevilo_nic = 0
    for x in range(len(list)):
        if list[x] != 0:
            kandidati.append(list[x])
            stevilo_nic = 0
        else:
            if len(kandidati) > 10:
                ton = np.median(np.array(kandidati))
                rezultat.append(float("{0:.2f}".format(ton)))
                kandidati =[]
            else:
                kandidati = []
    return rezultat

dir = "."
if len(sys.argv)== 2:
    dir = "./"+sys.argv[1]


# Prebere note v seznam
f = open("s.txt", "rt")
note_podatki = f.readline().strip().split(",")
for x in note_podatki:
    noteS.append(x)

f = open("a.txt", "rt")
note_podatki = f.readline().strip().split(",")
for x in note_podatki:
    noteA.append(x)

f = open("t.txt", "rt")
note_podatki = f.readline().strip().split(",")
for x in note_podatki:
    noteT.append(x)

f = open("b.txt", "rt")
note_podatki = f.readline().strip().split(",")
for x in note_podatki:
    noteB.append(x)

if not os.path.exists("rezultati_1"):
    os.makedirs("rezultati_1")


def posnetek(fname, note, min, max, cutoff):
    f = open("./rezultati_1/" +fname[:-4] + ".txt", "wt")
    f.write(fname + "\n")
    print "Obdelujem ",fname
    rezultati_frek, rezultati_note = obdelaj_posnetek(fname, 35, min, max, cutoff)
    print "rezultati: ", rezultati_note
    f.write(list_v_string(rezultati_note) + "\n") # v datoteke zapisan izracun not, filtrirani rezultati ter zdruzeni rezultati
    filtriraj_rezultate(rezultati_note,5)
    print "filtrirani rezultati: ", rezultati_note
    f.write(list_v_string(rezultati_note) + "\n")
    zdruzene_note = zdruzi_note(rezultati_note)
    print "zdruzene note: ", zdruzene_note
    rezultati_note = [] # pobrisem rezultate ki so bili pretvorjeni
    f.write(list_v_string(zdruzene_note) + "\n")
    f.close()
    print "not naj bi blo :", len(note), " not pa je :", len(zdruzene_note)
    if len(zdruzene_note) == len(note):
        print "OBDELAVA ", fname, " OK."
    else:
        print "OBDELAVA ", fname, " ERROR: STEVILO NOT SE NE UJEMA: ", (len(zdruzene_note) - len(note))
        # Dodati note v slovar
    if fname[:1]=="t":
        for i in range(len(zdruzene_note)):
            medianeT.append(zdruzene_note[i])
    elif fname[:1]=="s":
        for i in range(len(zdruzene_note)):
            medianeS.append(zdruzene_note[i])
    elif fname[:1]=="b":
        for i in range(len(zdruzene_note)):
            medianeB.append(zdruzene_note[i])
    elif fname[:1]=="a":
        for i in range(len(zdruzene_note)):
            medianeA.append(zdruzene_note[i])


posnetek("t.wav", noteT, 73, 880, 400)
posnetek("a.wav", noteA, 73, 880, 400)
posnetek("s.wav", noteS, 73, 880, 880)
posnetek("b.wav", noteB, 73, 880, 400)

f = open("./rezultati_1/MEDIANE.txt", "wt")

f.write("S;" + list_v_string(medianeS) + "\n")
f.write("A;" + list_v_string(medianeA) + "\n")
f.write("T;" + list_v_string(medianeT) + "\n")
f.write("B;" + list_v_string(medianeB) + "\n")
#zapis rezultatov
f.close()
print "Mediane shranjene."




