from tkinter import *
# mengimpor pustaka acak
import random

# Menambahkan variabel global

# variabel global
# pengaturan jendela
WIDTH = 900
HEIGHT = 300

#pengaturan raket

#lebar raket
PAD_W = 10
# tinggi raket
PAD_H = 100

#pengaturan bola
#Seberapa besar kecepatan bola akan meningkat dengan setiap pukulan
BALL_SPEED_UP = 1.05
#Kecepatan bola maksimum
BALL_MAX_SPEED = 48
# radius bola
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

#Skor pemain
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

#Menambahkan variabel global untuk jarak
#ke tepi kanan lapangan permainan
right_line_distance = WIDTH - PAD_W

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
    global BALL_X_SPEED
    #Letakkan bola di bagian tengah
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    #Atur arah bola ke arah pemain yang kalah,
    #tetapi mengurangi kecepatan ke kecepatan semula
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs (BALL_X_SPEED)

#fungsi bola pantul 
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    #memukul dengan raket if 
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs (BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

# memasang jendela
root = Tk()
root.title("Pong")

# area animasi
c = Canvas (root, width=WIDTH, height=HEIGHT, background="#003300") 
c.pack()

# elemen lapangan bermain

# garis kiri
c.create_line (PAD_W, 0, PAD_W, HEIGHT, fill="white")
# garis kanan
c.create_line (WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
# garis tengah
c.create_line (WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

#pemasangan fasilitas permainan

#membuat bola
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, 
                     HEIGHT/2-BALL_RADIUS/2, 
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="white")

# raket kiri
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")

# raket yang tepat
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, 
                          PAD_H, width=PAD_W, fill="yellow")

p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4,
                         text=PLAYER_1_SCORE, 
                         font="Arial 20",
                         fill="white")

p_2_text = c.create_text(WIDTH/6, PAD_H/4, 
                         text=PLAYER_2_SCORE, 
                         font="Arial 20",
                         fill="white")

#menambahkan variabel global untuk kecepatan bola
# di seluruh
BALL_X_CHANGE = 20
#secara vertikal
BALL_Y_CHANGE = 0

def move_ball():
    #menentukan koordinat sisi-sisi bola dan pusatnya
    ball_left, ball_top, ball_right, ball_bot = c.coords (BALL) 
    ball_center = (ball_top + ball_bot) / 2
    
    #pantulan vertikal
    #Jika kita berada jauh dari garis vertikal cukup gerakkan bola
    if ball_right + BALL_X_SPEED < right_line_distance and\
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    #Jika bola menyentuh sisi kanan atau kiri batas lapangan 
    elif ball_right == right_line_distance or ball_left == PAD_W:
        #Memeriksa sisi kanan atau kiri yang kita sentuh
        if ball_right > WIDTH /2:
            #Jika benar, bandingkan posisi bagian tengah bola
            #dengan posisi raket yang tepat.
            #Dan jika bola berada di dalam raket, lakukan pantulan
            if c. coords (RIGHT_PAD) [1] < ball_center< c. coords (RIGHT_PAD) [3]:
                bounce("strike")
            else:
                #Jika tidak, seorang pemain akan kehilangan kesempatan di sini kita tinggalkan operan untuk s 
                update_score("left") 
                spawn_ball()
        else:
            #Sama untuk pemain kidal
            if c. coords (LEFT_PAD) [1] < ball_center < c.coords (LEFT_PAD) [3]: 
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    #Periksa situasi di mana bola dapat terbang keluar dari batas lapangan permainan.
    #Dalam hal ini, cukup pindahkan ke tepi bidang.
    else:
        if ball_right > WIDTH /2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
    #pantulan horizontal
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

#mengatur variabel global untuk kecepatan raket
#kecepatan gerak raket yang akan dilalui
PAD_SPEED = 20
#kecepatan platform kiri
LEFT_PAD_SPEED = 0
#kecepatan raket yang tepat
RIGHT_PAD_SPEED=0

#fungsi pergerakan kedua raket
def move_pads():
    #Untuk kenyamanan, mari kita ciptakan kosakata di mana raket sesuai dengan kecepatannya 
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    # перебираем ракетки
    for pad in PADS:
        #menggerakkan raket dengan kecepatan tertentu
        c.move(pad, 0, PADS [pad])
        #jika raket bergerak keluar dari bidang permainan, letakkan kembali pada tempatnya
        if c.coords(pad) [1] < 0:
            c.move(pad, 0, c.coords(pad) [1])
        elif c.coords (pad) [3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords (pad) [3])

def main():
    move_ball()
    move_pads()
    #memanggil dirinya sendiri setiap 30 milidetik
    root.after(30, main)

#Mengatur fokus pada Canvas untuk merespons penekanan tombol
c. focus_set()

#Mari menulis fungsi untuk menangani penekanan tombol
def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Up":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        LEFT_PAD_SPEED = -PAD_SPEED

#Mengikat fungsi ini ke Canvas 
c.bind("<KeyPress>", movement_handler)

#Membuat fungsi respons pelepasan tombol
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in "ws":
        LEFT_PAD_SPEED=0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED=0

#Mari mengikat fungsi ini ke Canvas 
c.bind("<KeyRelease>", stop_pad)

#pengaturan dalam gerakan 
main()

#menjalankan jendela 
root.mainloop()