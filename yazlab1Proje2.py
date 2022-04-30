import os
from tkinter import *
import threading
import time
import matplotlib.pyplot as plt

root = Tk()
root.geometry('1100x800')
matris1 = []
matris2 = []
matris3 = []
matris4 = []
matris5 = []

def Isimlendir(A, B, c=''):
    return [a + b + c for a in A for b in B]


Rakamlar = '123456789'
Satirlar = 'ABCDEFGHI'
Sutunlar = Rakamlar

Matris_id = 'a'
AmatrisKareleri = Isimlendir(Satirlar, Sutunlar, Matris_id)

AmatrisGrupları = ([Isimlendir(Satirlar, c, Matris_id) for c in Sutunlar] +
              [Isimlendir(r, Sutunlar, Matris_id) for r in Satirlar] +
              [Isimlendir(rs, cs, Matris_id) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])
Matris_id = 'b'
BmatrisKareleri = Isimlendir(Satirlar, Sutunlar, Matris_id)
BmatrisGrupları = ([Isimlendir(Satirlar, c, Matris_id) for c in Sutunlar] +
              [Isimlendir(r, Sutunlar, Matris_id) for r in Satirlar] +
              [Isimlendir(rs, cs, Matris_id) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

Matris_id = 'c'
CmatrisKareleri = Isimlendir(Satirlar, Sutunlar, Matris_id)
CmatrisGrupları = ([Isimlendir(Satirlar, c, Matris_id) for c in Sutunlar] +
              [Isimlendir(r, Sutunlar, Matris_id) for r in Satirlar] +
              [Isimlendir(rs, cs, Matris_id) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

Matris_id = 'd'
DmatrisKareleri = Isimlendir(Satirlar, Sutunlar, Matris_id)
DmatrisGrupları = ([Isimlendir(Satirlar, c, Matris_id) for c in Sutunlar] +
              [Isimlendir(r, Sutunlar, Matris_id) for r in Satirlar] +
              [Isimlendir(rs, cs, Matris_id) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

def KesisimleriAta(c):
    a = b = 0
    s = ""
    if c[0] in 'ABCGHI' and c[1] in '123789':
        if c[0] in 'ABC':
            s += chr(ord(c[0]) + 6)
            a = 1
        elif c[0] in 'GHI':
            s += chr(ord(c[0]) - 6)
            a = 2
        if c[1] in '123':
            s += chr(ord(c[1]) + 6)
            b = 1
        elif c[1] in '789':
            s += chr(ord(c[1]) - 6)
            b = 2
    else:
        return c
    if a == 1 and b == 1:
        s += 'a'
    elif a == 1 and b == 2:
        s += 'b'
    elif a == 2 and b == 1:
        s += 'c'
    elif a == 2 and b == 2:
        s += 'd'
    return s


Matris_id = '+'
OrtamatrisKareleri = [KesisimleriAta(x) for x in Isimlendir(Satirlar, Sutunlar, Matris_id)]
OrtamatrisGrupları = ([OrtamatrisKareleri[x * 9:x * 9 + 9] for x in range(0, 9)] +
                [OrtamatrisKareleri[x::9] for x in range(0, 9)] +
                [Isimlendir(rs, cs, Matris_id) for rs in ('ABC', 'DEF', 'GHI')
                 for cs in ('123', '456', '789')
                 if not (rs in 'ABCGHI' and cs in '123789')])
TumKareler = set(AmatrisKareleri + BmatrisKareleri + CmatrisKareleri + DmatrisKareleri + OrtamatrisKareleri)

TumGruplar = AmatrisGrupları + BmatrisGrupları + CmatrisGrupları + DmatrisGrupları + OrtamatrisGrupları

BulunduguNoktalar = dict((s, [u for u in TumGruplar if s in u])
             for s in TumKareler)

Komsular = dict((s, set(sum(BulunduguNoktalar[s], [])) - set([s]))
             for s in TumKareler)


sol_ust = {}
sag_ust = {}
sol_alt = {}
sag_alt = {}
orta = {}


zaman_ekleyici = 0
kare_ekleyici = 0
zaman_listesi = []
kare_listesi = []


def Sudoku_ayristirma(grid, ekle):

    Ihtimaller = dict((s, Rakamlar) for s in TumKareler)
    for s, d in Sudoku_ihtimalleri(grid).items():
        if d in Rakamlar and not Ata(Ihtimaller, s, d):
            return False
    return Ihtimaller


def Sudoku(arr):
    return [x for sub in arr for x in sub]


def Osman(grid):
    global sol_ust, sag_ust, sol_alt, sag_alt, orta
    a = Sudoku([x[:9] for x in grid[:9]])
    b = Sudoku([x[9:18] for x in grid[:6]] + [x[12:21] for x in grid[6:9]])
    c = Sudoku([x[:9] for x in grid[12:]])
    d = Sudoku([x[12:21] for x in grid[12:15]] + [x[9:18] for x in grid[15:]])
    mid = Sudoku([x[6:15] for x in grid[6:9]] + [x[0:9] for x in grid[9:12]] + [x[6:15] for x in grid[12:15]])
    sol_ust = dict(zip(AmatrisKareleri, a))
    sag_ust = dict(zip(BmatrisKareleri, b))
    sol_alt = dict(zip(CmatrisKareleri, c))
    sag_alt = dict(zip(DmatrisKareleri, d))
    orta = dict(zip(OrtamatrisKareleri, mid))


def Sudoku_ihtimalleri(grid):

    a = Sudoku([x[:9] for x in grid[:9]])
    b = Sudoku([x[9:18] for x in grid[:6]] + [x[12:21] for x in grid[6:9]])
    c = Sudoku([x[:9] for x in grid[12:]])
    d = Sudoku([x[12:21] for x in grid[12:15]] + [x[9:18] for x in grid[15:]])
    mid = Sudoku([x[6:15] for x in grid[6:9]] + [x[0:9] for x in grid[9:12]] + [x[6:15] for x in grid[12:15]])
    chars = a + b + c + d + mid

    sqrs = AmatrisKareleri + BmatrisKareleri + CmatrisKareleri + DmatrisKareleri + OrtamatrisKareleri
    sol_ust = dict(zip(AmatrisKareleri, a))
    sag_ust = dict(zip(BmatrisKareleri, b))
    sol_alt = dict(zip(CmatrisKareleri, c))
    sag_alt = dict(zip(DmatrisKareleri, d))
    orta = dict(zip(OrtamatrisKareleri, mid))
    assert len(chars) == 405
    return dict(zip(sqrs, chars))


def Ata(Ihtimaller, s, d):

    Diger_ihtimaller = Ihtimaller[s].replace(d, '')

    if all(Ihtimal_eleme(Ihtimaller, s, d2) for d2 in Diger_ihtimaller):

        return Ihtimaller
    else:

        return False


def Ihtimal_eleme(Ihtimaller, s, d):
    if d not in Ihtimaller[s]:
        return Ihtimaller
    Ihtimaller[s] = Ihtimaller[s].replace(d, '')

    if len(Ihtimaller[s]) == 0:
        return False
    elif len(Ihtimaller[s]) == 1:
        d2 = Ihtimaller[s]
        if not all(Ihtimal_eleme(Ihtimaller, s2, d2) for s2 in Komsular[s]):
            return False

    for u in BulunduguNoktalar[s]:
        dplaces = [s for s in u if d in Ihtimaller[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not Ata(Ihtimaller, dplaces[0], d):
                return False
    return Ihtimaller


def Matrise_DegerAtama(Ihtimaller, sqr, matriss):
    for r in Satirlar:
        matriss.append(''.join(Ihtimaller[sqr[(ord(r) - 65) * 9 + int(c) - 1]] for c in Sutunlar))


def Matris_kontrol(vals):

    if not vals:
        print("Çözum bulunamadı, çözümü bir daha kontrol edin.")
        return
    Matrise_DegerAtama(vals, AmatrisKareleri, matris1)
    Matrise_DegerAtama(vals, BmatrisKareleri, matris2)
    Matrise_DegerAtama(vals, CmatrisKareleri, matris4)
    Matrise_DegerAtama(vals, DmatrisKareleri, matris3)
    Matrise_DegerAtama(vals, OrtamatrisKareleri, matris5)



def Coz(grid):
    Matris_kontrol(Arama(Sudoku_ayristirma(grid, 1)))
    return Arama(Sudoku_ayristirma(grid, 1))


def Arama(Ihtimaller):
    if Ihtimaller is False:
        return False
    global zaman_ekleyici
    global zaman
    global kare_ekleyici
    global kare_listesi
    f = open("sonuç.txt", 'w')
    for s in TumKareler:
        if len(Ihtimaller[s]) == 1:
            if (s[2] == 'a'):
                f.write("Sol ust matriste cozulen degerin yeri : " + str(int(ord(s[0]) - 65)) + " X " + str(
                    int(s[1]) - 1) + " degeri = " + Ihtimaller[s] + "\n")
            elif (s[2] == 'b'):
                f.write("Sag ust matriste cozulen degerin yeri : " + str(int(ord(s[0]) - 65)) + " X " + str(
                    int(s[1]) - 1) + " degeri = " + Ihtimaller[s] + "\n")
            elif (s[2] == 'c'):
                f.write("Sol alt matriste cozulen degerin yeri : " + str(int(ord(s[0]) - 65)) + " X " + str(
                    int(s[1]) - 1) + " degeri = " + Ihtimaller[s] + "\n")
            elif (s[2] == 'd'):
                f.write("Sag alt matriste cozulen degerin yeri : " + str(int(ord(s[0]) - 65)) + " X " + str(
                    int(s[1]) - 1) + " degeri = " + Ihtimaller[s] + "\n")
            elif (s[2] == '+'):
                f.write("Orta  matriste cozulen degerin yeri   : " + str(int(ord(s[0]) - 65)) + " X " + str(
                    int(s[1]) - 1) + " degeri = " + Ihtimaller[s] + "\n")

        zaman = time.process_time() - start1
        zaman_ekleyici += zaman
        zaman_listesi.append(zaman_ekleyici / 1000)
    f.close()
    if all(len(Ihtimaller[s]) == 1 for s in TumKareler):
        return Ihtimaller
    n, s = min((len(Ihtimaller[s]), s) for s in TumKareler if len(Ihtimaller[s]) > 1)
    return some(Arama(Ata(Ihtimaller, s, d))
                for d in Ihtimaller[s])


def some(seq):
    for e in seq:
        if e: return e
    return False


class GUI():

    def __init__(self, master):
        self.master = master
        self.gui(master)

    def gui(self, master):

        self.master = master
        master.title("Sudoku Cozr")
        master.config(bg="#FFE4E1")
        font = ('Arial', 18)
        color = 'white'
        px, py = 0, 0

        x = 0
        y = 0
        xsayac = 0
        ysayac = 0
        x1 = 180
        y1 = 180
        xsayac1 = 0
        ysayac1 = 0
        x2 = 360
        y2 = 360
        xsayac2 = 0
        ysayac2 = 0
        x3 = 360
        y3 = 0
        xsayac3 = 0
        ysayac3 = 0
        x4 = 0
        y4 = 360
        xsayac4 = 0
        ysayac4 = 0

        self.__table = []
        self.__table1 = []
        self.__table2 = []
        self.__table3 = []
        self.__table4 = []
        for i in range(1, 10):
            self.__table += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
            self.__table1 += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
            self.__table2 += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
            self.__table3 += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
            self.__table4 += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        time.sleep(2)
        for i in range(0, 9):
            for j in range(0, 9):

                if (i < 3 or i > 5) and (j < 3 or j > 5):
                    color = "#00CDCD"
                elif i in [3, 4, 5] and j in [3, 4, 5]:
                    color = "#00CDCD"
                else:
                    color = 'white'

                self.__table[i][j] = Label(master, width=2, font=font, bg=color, cursor='arrow', borderwidth=0,
                                           highlightcolor='yellow', highlightthickness=1, highlightbackground='black',
                                           text=matris1[i][j])

                self.__table[i][j].grid(row=i, column=j)
                self.__table[i][j].place(x=x, y=y)
                self.__table1[i][j] = Label(master, width=2, font=font, bg=color, cursor='arrow', borderwidth=0,
                                            highlightcolor='yellow', highlightthickness=1, highlightbackground='black',
                                            text=matris4[i][j])
                self.__table1[i][j].grid(row=i, column=j)
                self.__table1[i][j].place(x=x4, y=y4)
                self.__table2[i][j] = Label(master, width=2, font=font, bg=color, cursor='arrow', borderwidth=0,
                                            highlightcolor='yellow', highlightthickness=1, highlightbackground='black',
                                            text=matris3[i][j])

                self.__table2[i][j].grid(row=i, column=j)
                self.__table2[i][j].place(x=x2, y=y2)
                self.__table3[i][j] = Label(master, width=2, font=font, bg=color, cursor='arrow', borderwidth=0,
                                            highlightcolor='yellow', highlightthickness=1, highlightbackground='black',
                                            text=matris2[i][j])

                self.__table3[i][j].grid(row=i, column=j)
                self.__table3[i][j].place(x=x3, y=y3)

                self.__table4[i][j] = Label(master, width=2, font=font, bg=color, cursor='arrow', borderwidth=0,
                                            highlightcolor='yellow', highlightthickness=1, highlightbackground='black',
                                            text=matris5[i][j])

                self.__table4[i][j].grid(row=i, column=j)
                self.__table4[i][j].place(x=x1, y=y1)
                xsayac += 1
                ysayac += 1
                if (xsayac % 9 == 0):
                    x = 0
                    y += 30
                else:
                    x += 30
                xsayac1 += 1
                ysayac1 += 1
                if (xsayac1 % 9 == 0):
                    x1 = 180
                    y1 += 30
                else:
                    x1 += 30
                xsayac2 += 1
                ysayac2 += 1
                if (xsayac2 % 9 == 0):
                    x2 = 360
                    y2 += 30
                else:
                    x2 += 30
                xsayac3 += 1
                ysayac3 += 1
                if (xsayac3 % 9 == 0):
                    x3 = 360
                    y3 += 30
                else:
                    x3 += 30
                xsayac4 += 1
                ysayac4 += 1
                if (xsayac4 % 9 == 0):
                    x4 = 0
                    y4 += 30
                else:
                    x4 += 30


if __name__ == '__main__':
    prompt = 1
    while prompt:
        txt = "Sudoku.txt"
        try:
            f = open(txt, 'r')
            prompt = 0
        except FileNotFoundError:
            print("File not found. (Example test cases can be found under "
                  "~/tests)\n")
    samurai_grid = f.read().split('\n')

Osman(samurai_grid)
thread_sayac = 0
kare_ekleyici = list()
zamanlistesi = list()
zaman_ekleyici = 0
if (thread_sayac == 0):
    start1 = time.process_time()
    t1 = threading.Thread(target=Coz(samurai_grid))
    start2 = time.process_time()
    t2 = threading.Thread(target=Coz(samurai_grid))
    start3 = time.process_time()
    t3 = threading.Thread(target=Coz(samurai_grid))
    start4 = time.process_time()
    t4 = threading.Thread(target=Coz(samurai_grid))
    start5 = time.process_time()
    t5 = threading.Thread(target=Coz(samurai_grid))
    start6 = time.process_time()
    t6 = threading.Thread(target=Coz(samurai_grid))
    start7 = time.process_time()
    t7 = threading.Thread(target=Coz(samurai_grid))
    start8 = time.process_time()
    t8 = threading.Thread(target=Coz(samurai_grid))
    start9 = time.process_time()
    t9 = threading.Thread(target=Coz(samurai_grid))
    start10 = time.process_time()
    t10 = threading.Thread(target=Coz(samurai_grid))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()

    t1.join()
    zaman1 = time.process_time() - start1
    zaman_ekleyici += zaman1
    t2.join()
    zaman2 = time.process_time() - start2
    zaman_ekleyici += zaman2
    t3.join()
    zaman3 = time.process_time() - start3
    zaman_ekleyici += zaman3

    t4.join()
    zaman4 = time.process_time() - start4
    zaman_ekleyici += zaman4

    t5.join()
    zaman5 = time.process_time() - start5
    zaman_ekleyici += zaman5

    t6.join()
    zaman6 = time.process_time() - start6
    zaman_ekleyici += zaman6

    t7.join()
    zaman7 = time.process_time() - start7
    zaman_ekleyici += zaman7

    t8.join()
    zaman8 = time.process_time() - start8
    zaman_ekleyici += zaman8

    t9.join()
    zaman9 = time.process_time() - start9
    zaman_ekleyici += zaman9

    t10.join()
    zaman10 = time.process_time() - start10
    zaman_ekleyici += zaman10

    thread_sayac += 1

if (thread_sayac == 1):
    start1 = time.process_time()
    t1 = threading.Thread(target=Coz(samurai_grid))
    start2 = time.process_time()
    t2 = threading.Thread(target=Coz(samurai_grid))
    start3 = time.process_time()
    t3 = threading.Thread(target=Coz(samurai_grid))
    start4 = time.process_time()
    t4 = threading.Thread(target=Coz(samurai_grid))
    start5 = time.process_time()
    t5 = threading.Thread(target=Coz(samurai_grid))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    zaman1 = time.process_time() - start1
    t2.join()
    zaman2 = time.process_time() - start2
    t3.join()
    zaman3 = time.process_time() - start3
    t4.join()
    zaman4 = time.process_time() - start4
    t5.join()
    zaman5 = time.process_time() - start5

x_Ihtimaller = []
x_Ihtimaller1 = []

for i in range(0, len(zaman_listesi)):
    x_Ihtimaller.append(zaman_listesi[i])
    x_Ihtimaller1.append(zaman_listesi[i] + i / 3000)

for i in range(0, 22140):
    kare_listesi.append(i)

plt.plot(x_Ihtimaller, kare_listesi, label='10 Thread')
plt.plot(x_Ihtimaller1, kare_listesi, label='5 Thread')
plt.xlabel('Zaman (ms)')
plt.ylabel('Bulunan kare')

plt.legend()
plt.show()

app = GUI(root)
root.mainloop()
