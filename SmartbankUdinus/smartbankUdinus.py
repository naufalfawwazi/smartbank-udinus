from tkinter import Tk,messagebox
from tkinter.ttk import Label,Button,Entry,Style
import sqlite3
import smtplib

def select(query):
	connection = sqlite3.connect('smartbank.db')
	cursor = connection.cursor()

	cursor.execute(query)
	hasil =  cursor.fetchall()

	cursor.close()
	connection.close()
	return hasil

def insert(data):
	connection = sqlite3.connect('smartbank.db')
	cursor = connection.cursor()

	query = "INSERT INTO users(Nama,NIM,PIN) VALUES(?,?,?);"
	cursor.execute(query,data)

	connection.commit()
	cursor.close()
	connection.close()

def update(total,nim):
	connection = sqlite3.connect('smartbank.db')
	cursor = connection.cursor()

	query = f"Update users set Saldo=Saldo+{total} where NIM = '{nim}'"
	cursor.execute(query)

	connection.commit()
	cursor.close()
	connection.close()

def send_email(namapenerima, emailtujuan, kode):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    isi = f"""From: SmartBank UDINUS <from@fromdomain.com>
To: {namapenerima} <{emailtujuan}>
MIME-Version: 1.0
Content-type: text/html
Subject: Kode Konfirmasi SmartBank UDINUS

<h2>Selamat Datang di SmartBank UDINUS!</h2>
<h2>Berikut adalah Kode Konfirmasi Pendaftaran Anda</h2>
<hr><hr>
<h5><i>Jika anda tidak merasa mendaftar SmartBank UDINUS, <a href="https://t.me/naufalfawwazi" target="_blank">laporkan disini.</a></i></h5>
<br><br>
<h1>{kode}</h1>
<br>
<br>"""             
    sender = "EMAIL_UNTUK_MENGIRIM"
    pwd = "PASSWORD_EMAIL_UNTUK_MENGIRIM"
    server.login(sender,pwd)
    server.sendmail(sender,emailtujuan,isi)

class WindowLogin(Tk):
    def __init__(self):
        super().__init__()

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('280x172')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Halaman Login SmartBank UDINUS', style='TLabel', font=('Helvetica', 11))
        self.lblJudul.grid(row=0, column=0, columnspan=3, pady=10, sticky='n') 

        self.lblNIM = Label(self, text='NIM\t:', width=10, anchor='w', style='TLabel')
        self.lblNIM.grid(row=1, column=0, padx=8)

        self.lblPIN = Label(self, text='PIN\t:', width=10, anchor='w', style='TLabel')
        self.lblPIN.grid(row=2, column=0, padx=8)

        self.lblRegister = Label(self, text='Belum punya akun?', anchor='e', style='TLabel')
        self.lblRegister.grid(row=3, column=1, sticky='e')

        #deklarasi entry
        self.entNIM = Entry(self)
        self.entNIM.grid(row=1, column=1, columnspan=2, ipadx=32, sticky='w', pady=3)

        self.entPIN = Entry(self, show='*')
        self.entPIN.grid(row=2, column=1, columnspan=2, ipadx=32, sticky='w', pady=3)

        #deklarasi button
        self.btnLogin = Button(self, text='Login', width=7, command=self.Login, style='TButton')
        self.btnLogin.grid(row=3, column=0, pady=10, sticky='w', padx=8)

        self.buttonRegister = Button(self, text='Register', style='TButton', command=self.Register)
        self.buttonRegister.grid(row=3, column=2, padx=8, sticky='w')

        self.buttonHelp = Button(self, text='Help', style='TButton', command=self.Help)
        self.buttonHelp.grid(row=4, column=0, padx=8, ipadx=95, columnspan=3)

    def Login(self):
        kodejurusan = [
            'A11','A12','A14','A21','A22','A23','A24','B11','B12','B21','C11','C12','C21','C23','D11','D22','E11','E12'
        ]
        angka = [
            '1','2','3','4','5','6','7','8','9','0'
        ]
        nim = self.entNIM.get().capitalize()
        pin = self.entPIN.get()
        query1 = f'select Nama, NIM, PIN, Saldo from users where NIM="{nim}"'
        data1 = select(query1)
        query = f'select Nama, NIM, PIN, Saldo from users where NIM="{nim}" and PIN="{pin}"'
        data = select(query)
        if nim != "" and pin != "" :
            if nim[0:3] in kodejurusan and len(nim) == 14 and nim[3] == '.' and nim[8] == '.' :
                if len(pin) == 5 and pin[0] and pin[1] and pin[2] and pin[3] and pin[4] in angka :
                    if data1 :
                        if data :
                            messagebox.showinfo('Berhasil', 'Berhasil Login')
                            self.destroy()
                            libs = WindowMenu(*data)
                            libs.mainloop()
                        else :
                            messagebox.showerror('Kesalahan', 'PIN Salah')
                    else :
                        messagebox.showerror('Kesalahan', 'NIM belum terdaftar')
                else :
                    messagebox.showerror('Kesalahan', 'Format PIN Salah')
            else :
                messagebox.showerror('Kesalahan', 'Format NIM Salah')
        else :
            messagebox.showwarning('Kesalahan', 'Masukkan NIM dan PIN')
    
    def Register(self):
        self.destroy()
        WindowRegister()

    def Help(self):
        messagebox.showinfo('Bantuan', 'Kolom NIM diisi dengan format XXX.YYYY.ZZZZZ\nXXX\t: Kode Jurusan Mahasiswa\nYYYY\t: Tahun Pendaftaran Mahasiswa\nZZZZZ\t: Nomor Urut Mahasiswa\nContoh\t: A11.2020.12764\n\nKolom PIN diisi dengan format 5 digit angka\nContoh\t: 11111')

class WindowRegister(Tk):
    def __init__(self):
        super().__init__()

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('280x198')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Halaman Register SmartBank UDINUS', style='TLabel', font=('Helvetica', 11))
        self.lblJudul.grid(row=0, column=0, columnspan=3, pady=10, sticky='n') 

        self.lblNama = Label(self, text='Nama\t:', width=10, anchor='w', style='TLabel')
        self.lblNama.grid(row=1, column=0, padx=8)

        self.lblNIM = Label(self, text='NIM\t:', width=10, anchor='w', style='TLabel')
        self.lblNIM.grid(row=2, column=0, padx=8)

        self.lblPIN = Label(self, text='PIN\t:', width=10, anchor='w', style='TLabel')
        self.lblPIN.grid(row=3, column=0, padx=8)

        self.lblRegister = Label(self, text='Sudah punya akun?', anchor='e', style='TLabel')
        self.lblRegister.grid(row=4, column=1, sticky='e')

        #deklarasi entry
        self.entNama = Entry(self)
        self.entNama.grid(row=1, column=1, columnspan=2, ipadx=32, sticky='w', pady=3)

        self.entNIM = Entry(self)
        self.entNIM.grid(row=2, column=1, columnspan=2, ipadx=32, sticky='w', pady=3)

        self.entPIN = Entry(self, show='*')
        self.entPIN.grid(row=3, column=1, columnspan=2, ipadx=32, sticky='w', pady=3)

        #deklarasi button
        self.btnLogin = Button(self, text='Register', width=7, command=self.Register, style='TButton')
        self.btnLogin.grid(row=4, column=0, pady=10, sticky='w', padx=8)

        self.buttonRegister = Button(self, text='Login', style='TButton', command=self.Login)
        self.buttonRegister.grid(row=4, column=2, padx=8, sticky='e')
        
        self.buttonHelp = Button(self, text='Help', style='TButton', command=self.Help)
        self.buttonHelp.grid(row=5, column=0, padx=8, ipadx=95, columnspan=3)

    def Register(self):
        kodejurusan = [
            'A11','A12','A14','A21','A22','A23','A24','B11','B12','B21','C11','C12','C21','C23','D11','D22','E11','E12'
        ]
        angka = [
            '1','2','3','4','5','6','7','8','9','0'
        ]
        kode_email = {
            'A':'1','B':'2','C':'3','D':'4','E':'5'
        }
        nama = self.entNama.get().title()
        nim = self.entNIM.get().capitalize()
        pin = self.entPIN.get()
        query = f'select Nama, NIM, PIN, Saldo from users where NIM="{nim}"'
        data = select(query)
        email = f"{nim.replace('.','').replace(nim[0],kode_email.get(nim[0]))}@mhs.dinus.ac.id"
        from random import randint
        KodeKonfirmasi = f'SMRTBNK-{randint(11111,99999)}'
        akun = [(nama,nim,pin,email,KodeKonfirmasi)]

        if nama != "" and nim != "" and pin != "" :
            if nim[0:3] in kodejurusan and len(nim) == 14 and nim[3] == '.' and nim[8] == '.' :
                if len(pin) == 5 and pin[0] and pin[1] and pin[2] and pin[3] and pin[4] in angka :
                    if data :
                        messagebox.showerror('Kesalahan', 'NIM sudah terdaftar')
                    else :
                        self.entNama.delete(0,'end')
                        self.entNIM.delete(0,'end')
                        self.entPIN.delete(0,'end')
                        messagebox.showinfo('Konfirmasi', 'Kode Konfirmasi telah dikirimkan ke email mahasiswa anda\nAnda akan dialihkan ke halaman Konfirmasi')
                        send_email(nama, email, KodeKonfirmasi)
                        self.destroy()
                        libs = WindowKonfirmasi(*akun)
                        libs.mainloop()
                else :
                    messagebox.showerror('Kesalahan', 'Format PIN Salah')
            else :
                messagebox.showerror('Kesalahan', 'Format NIM Salah')
        else :
            messagebox.showwarning('Kesalahan', 'Masukkan Nama, NIM dan PIN')
    
    def Login(self):
        self.destroy()
        WindowLogin()
    
    def Help(self):
        messagebox.showinfo('Bantuan', 'Kolom Nama diisi dengan Nama Lengkap\nContoh\t: Naufal Fawwazi\n\nKolom NIM diisi dengan format XXX.YYYY.ZZZZZ\nXXX\t: Kode Jurusan Mahasiswa\nYYYY\t: Tahun Pendaftaran Mahasiswa\nZZZZZ\t: Nomor Urut Mahasiswa\nContoh\t: A11.2020.12764\n\nKolom PIN diisi dengan format 5 digit angka\nContoh\t: 11111')

class WindowKonfirmasi(Tk):
    def __init__(self, akun):
        super().__init__()

        self.nama = akun[0] 
        self.nim = akun[1]
        self.pin = akun[2]
        self.email = akun[3]
        self.KodeKonfirmasi = akun[4]

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('235x195')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Halaman Konfirmasi Pendaftaran', anchor='center', style='TLabel', font=('Helvetica', 11))
        self.lblJudul.grid(row=0, column=0, padx=8, pady=(10,2)) 

        self.lblJudul2 = Label(self, text='SmartBank UDINUS', anchor='center', style='TLabel', font=('Helvetica', 11))
        self.lblJudul2.grid(row=1, column=0, padx=8, pady=(1,10)) 

        self.lblKode = Label(self, text='Kode Konfirmasi:', anchor='center', style='TLabel')
        self.lblKode.grid(row=2, column=0, columnspan=2, padx=8)

        #deklarasi entry
        self.entKode = Entry(self)
        self.entKode.grid(row=3, column=0, ipadx=32, sticky='n', padx=8, pady=3)

        #deklarasi button
        self.btnLogin = Button(self, text='Kirim', width=7, command=self.Kirim, style='TButton')
        self.btnLogin.grid(row=4, column=0, pady=2, sticky='n', padx=8)
        
        self.buttonHelp = Button(self, text='Help', style='TButton', command=self.Help)
        self.buttonHelp.grid(row=5, column=0, padx=8, pady=20, ipadx=71)

    def Kirim(self):
        if self.entKode.get() == self.KodeKonfirmasi :
            self.entKode.delete(0,'end')
            insert([self.nama, self.nim, self.pin])
            messagebox.showinfo('Berhasil', 'Berhasil Register\nAnda akan dialihkan ke halaman Login')
            self.destroy()
            WindowLogin()
        else :
            self.entKode.delete(0,'end')
            messagebox.showerror('Kesalahan','Kode konfirmasi yang anda masukkan salah')

    def Help(self):
        messagebox.showinfo('Bantuan', f'Email Mahasiswa Anda : {self.email}\n\nMasukkan kode konfirmasi yang telah dikirimkan ke email mahasiswa anda.\nFormat\t: SMRTBNK-XXXXX\nContoh\t: SMRTBNK-12345\n\nJika masih belum mendapatkan kode konfirmasi, periksa folder spam/sampah pada email anda.')

class WindowMenu(Tk):
    def __init__(self, data):
        super().__init__()

        listjurusan = {
            'A11' : 'Teknik Informatika (S1)', 'A12' : 'Sistem Informasi (S1)', 'A14' : 'Desain Komunikasi Visual (S1)',
            'A21' : 'Manajemen Informatika (D3)', 'A22' : 'Teknik Informatika (D3)', 'A23' : 'Komputerisasi akuntansi (D3)',
            'A24' : 'Broadcasting (D3)', 'B11' : 'Manajemen (S1)', 'B12' : 'Akuntansi (S1)', 'B21' : 'Akuntansi (D3)', 
            'C11' : 'Sastra Inggris (S1)', 'C12' : 'Sastra Jepang (S1)', 'C21' : 'Bahasa Inggris (D3)', 'C23' : 'Bahasa Cina (D3)',
            'D11' : 'Kesehatan Masyarakat (S1)', 'D22' : 'Rekam medis & Info Kesehatan (D3)', 'E11' : 'Teknik Elektro (S1)',
            'E12' : 'Teknik Industri (S1)'
        }

        self.nama = data[0]
        self.nim = data[1]
        self.pin = data[2]
        self.saldo = data[3]
        self.jurusan = listjurusan.get(self.nim[0:3])
        saldotampil = f'{self.saldo:,}'
        saldotampil = saldotampil.replace(',','.')
        data = [data]
        
        #deklarasi windows 
        self.title('SmartBank UDINUS')
        self.geometry('395x467')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff', font=('Cambria',15))
        Style().configure('menu.TLabel', foreground='black', background='#89d1ff', font=('Cambria',20)) 
        Style().configure('TButton', foreground='black', background='black')
        Style().configure('menu.TButton', foreground='black', background='black', font=('Cambria',20))

        #deklarasi label
        self.labelSalam = Label(self, text=f'Selamat datang {self.nama}', style='TLabel')
        self.labelSalam.grid(row=0, column=0, padx=8, columnspan=2, sticky='w')

        self.labelJurusan = Label(self, text=f'Mahasiswa {self.jurusan}', style='TLabel')
        self.labelJurusan.grid(row=1, column=0, padx=8, columnspan=2, sticky='w')

        self.labelSaldo = Label(self, text=f'Saldo anda Rp {saldotampil},-', style='TLabel')
        self.labelSaldo.grid(row=2, column=0, padx=8, columnspan=2, sticky='w')

        self.labelMenu = Label(self, text='MENU', style='menu.TLabel')
        self.labelMenu.grid(row=3, column=0, padx=8, columnspan=2, pady=20)

        #deklarasi button
        self.buttonDeposit = Button(self, text='Deposit', style='menu.TButton', width=10, command=self.Deposit)
        self.buttonDeposit.grid(row=4, column=0, padx=(10,5), pady=5, ipadx=10, ipady=37, sticky='w')

        self.buttonTarikSaldo = Button(self, text='Tarik Saldo', style='menu.TButton', width=10, command=self.TarikSaldo)
        self.buttonTarikSaldo.grid(row=4, column=1, padx=5, pady=5, ipadx=10, ipady=37, sticky='w')

        self.buttonStatus = Button(self, text='     Status\nKeanggotaan', style='menu.TButton', width=10, command=self.Status)
        self.buttonStatus.grid(row=5, column=0, padx=(10,5), pady=5, ipadx=10, ipady=20, sticky='w')

        self.buttonTransferSaldo = Button(self, text='Transfer Saldo', style='menu.TButton', width=10, command=self.TransferSaldo)
        self.buttonTransferSaldo.grid(row=5, column=1, padx=5, pady=5, ipadx=10, ipady=37, sticky='w')

        self.buttonKeluar = Button(self, text='Keluar', style='menu.TButton', width=23, command=self.Keluar)
        self.buttonKeluar.grid(row=6, column=0, columnspan=2, padx=10, pady=5, ipadx=10, ipady=1, sticky='w')

    def Deposit(self):
        messagebox.showinfo('Deposit', 'Anda akan diarahkan ke halaman Deposit')
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        self.destroy()
        libs = WindowDeposit(*data)
        libs.mainloop()

    def TarikSaldo(self):
        messagebox.showinfo('Penarikan Saldo', 'Anda akan diarahkan ke halaman Penarikan Saldo')
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        self.destroy()
        libs = WindowTarikSaldo(*data)
        libs.mainloop()

    def Status(self):
        messagebox.showinfo('Status Keanggotaan', 'Anda akan diarahkan ke halaman Status Keanggotaan')
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        self.destroy()
        libs = WindowStatus(*data)
        libs.mainloop()

    def TransferSaldo(self):
        messagebox.showinfo('Transfer Saldo', 'Anda akan diarahkan ke halaman Transfer Saldo')
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        self.destroy()
        libs = WindowTransferSaldo(*data)
        libs.mainloop()

    def Keluar(self):
        messagebox.showinfo('Terima Kasih', 'Terima kasih telah menggunakan SmartBank UDINUS\nSemoga hari anda menyenangkan')
        self.destroy()

class WindowDeposit(Tk):
    def __init__(self, data):
        super().__init__()
        
        self.nama = data[0]
        self.nim = data[1]
        self.pin = data[2]
        self.saldo = data[3]
        saldotampil = f'{self.saldo:,}'
        saldotampil = saldotampil.replace(',','.')

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('332x188')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Deposit', style='TLabel', font=('Helvetica', 11))
        self.lblJudul.grid(row=0, column=0, columnspan=4, pady=10) 

        self.lblNominal = Label(self, text='Nominal Deposit\t\t:', style='TLabel')
        self.lblNominal.grid(row=1, column=0, padx=8, sticky='w')

        self.labelRupiah = Label(self, text='Rp', style='TLabel')
        self.labelRupiah.grid(row=1, column=1, sticky='w')

        self.labelSatuan = Label(self, text=',-', style='TLabel')
        self.labelSatuan.grid(row=1, column=3, sticky='w')
    
        self.lblPINKonfirmasi = Label(self, text='Konfirmasi PIN Anda\t:', style='TLabel')
        self.lblPINKonfirmasi.grid(row=2, column=0, padx=8, sticky='w')

        #deklarasi entry
        self.entryNominal = Entry(self)
        self.entryNominal.grid(row=1, column=2, sticky='w', pady=3)

        self.entryPINKonfirmasi = Entry(self, show='*')
        self.entryPINKonfirmasi.grid(row=2, column=2, columnspan=3, sticky='w', pady=3)

        #deklarasi button
        self.buttonDeposit = Button(self, text='Deposit', style='TButton', command=self.Deposit)
        self.buttonDeposit.grid(row=3, column=0, columnspan=4, pady=5)

        self.buttonKembali = Button(self, text='Menu', style='TButton', command=self.Menu)
        self.buttonKembali.grid(row=4, column=0, padx=8, pady=5, sticky='w')

        self.buttonKeluar = Button(self, text='Keluar', style='TButton', command=self.Keluar)
        self.buttonKeluar.grid(row=4, column=2, columnspan=3, pady=5, sticky='e')

        self.lblSaldo = Label(self, text=f'Saldo anda saat ini\t: Rp {saldotampil},-', style='TLabel')
        self.lblSaldo.grid(row=5, column=0, columnspan=4, padx=8, sticky='w')
    
    def Deposit(self):
        if self.entryNominal.get() != '' and self.entryPINKonfirmasi.get() != '' :
            nominal = f'{self.entryNominal.get()}'
            if '.' in nominal :
                if ',' in nominal :
                    nominal = nominal.replace('.','')
                    nominal = nominal.replace(',','')
                    nominal = eval(nominal)  
                else :
                    nominal = nominal.replace('.','')
                    nominal = eval(nominal)  
            elif ',' in nominal :
                if '.' in nominal :
                    nominal = nominal.replace(',','')
                    nominal = nominal.replace('.','')
                    nominal = eval(nominal)  
                else :
                    nominal = nominal.replace(',','')
                    nominal = eval(nominal)  
            else :
                nominal = eval(nominal)
            if self.entryPINKonfirmasi.get() == self.pin :
                self.saldo += nominal
                update(+nominal, self.nim)
                self.entryNominal.delete(0,'end')
                self.entryPINKonfirmasi.delete(0,'end')
                saldotampil = f'{self.saldo:,}'
                saldotampil = saldotampil.replace(',','.')
                nominaltampil = f'{nominal:,}'
                nominaltampil = nominaltampil.replace(',','.')
                self.lblSaldo.destroy()
                self.lblSaldo = Label(self, text=f'Saldo anda saat ini\t: Rp {saldotampil},-', style='TLabel')
                self.lblSaldo.grid(row=5, column=0, columnspan=4, padx=8, sticky='w')
                messagebox.showinfo('Berhasil', f'Deposit sebesar Rp {nominaltampil},- telah berhasil')
            else :
                messagebox.showerror('Kesalahan', 'PIN Salah')
        else :
            messagebox.showerror('Kesalahan','Terdeteksi form kosong')

    def Menu(self):
        self.destroy()
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        libs = WindowMenu(*data)
        libs.mainloop()

    def Keluar(self):
        messagebox.showinfo('Terima Kasih', 'Terima kasih telah menggunakan SmartBank UDINUS\nSemoga hari anda menyenangkan')
        self.destroy()

class WindowTarikSaldo(Tk):
    def __init__(self, data):
        super().__init__()
        
        self.nama = data[0]
        self.nim = data[1]
        self.pin = data[2]
        self.saldo = data[3]
        saldotampil = f'{self.saldo:,}'
        saldotampil = saldotampil.replace(',','.')

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('332x188')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Penarikan Saldo', style='TLabel', font=('Helvetica', 11))
        self.lblJudul.grid(row=0, column=0, columnspan=4, pady=10) 

        self.lblNominal = Label(self, text='Nominal Penarikan\t:', style='TLabel')
        self.lblNominal.grid(row=1, column=0, padx=8, sticky='w')

        self.labelRupiah = Label(self, text='Rp', style='TLabel')
        self.labelRupiah.grid(row=1, column=1, sticky='w')

        self.labelSatuan = Label(self, text=',-', style='TLabel')
        self.labelSatuan.grid(row=1, column=3, sticky='w')
    
        self.lblPINKonfirmasi = Label(self, text='Konfirmasi PIN Anda\t:', style='TLabel')
        self.lblPINKonfirmasi.grid(row=2, column=0, padx=8, sticky='w')

        #deklarasi entry
        self.entryNominal = Entry(self)
        self.entryNominal.grid(row=1, column=2, sticky='w', pady=3)

        self.entryPINKonfirmasi = Entry(self, show='*')
        self.entryPINKonfirmasi.grid(row=2, column=2, columnspan=3, sticky='w', pady=3)

        #deklarasi button
        self.buttonTarikSaldo = Button(self, text='Tarik Saldo', style='TButton', command=self.TarikSaldo)
        self.buttonTarikSaldo.grid(row=3, column=0, columnspan=4, pady=5)

        self.buttonKembali = Button(self, text='Menu', style='TButton', command=self.Menu)
        self.buttonKembali.grid(row=4, column=0, padx=8, pady=5, sticky='w')

        self.buttonKeluar = Button(self, text='Keluar', style='TButton', command=self.Keluar)
        self.buttonKeluar.grid(row=4, column=2, columnspan=3, pady=5, sticky='e')

        self.lblSaldo = Label(self, text=f'Saldo anda saat ini\t: Rp {saldotampil},-', style='TLabel')
        self.lblSaldo.grid(row=5, column=0, columnspan=4, padx=8, sticky='w')
    
    def TarikSaldo(self):
        if self.entryNominal.get() != '' and self.entryPINKonfirmasi.get() != '' :
            nominal = f'{self.entryNominal.get()}'
            if '.' in nominal :
                if ',' in nominal :
                    nominal = nominal.replace('.','')
                    nominal = nominal.replace(',','')
                    nominal = eval(nominal)  
                else :
                    nominal = nominal.replace('.','')
                    nominal = eval(nominal)  
            elif ',' in nominal :
                if '.' in nominal :
                    nominal = nominal.replace(',','')
                    nominal = nominal.replace('.','')
                    nominal = eval(nominal)  
                else :
                    nominal = nominal.replace(',','')
                    nominal = eval(nominal)  
            else :
                nominal = eval(nominal)
            if self.entryPINKonfirmasi.get() == self.pin :
                if nominal <= self.saldo :
                    if nominal % 50000 == 0 :
                        self.saldo -= nominal
                        update(-nominal, self.nim)
                        self.entryNominal.delete(0,'end')
                        self.entryPINKonfirmasi.delete(0,'end')
                        saldotampil = f'{self.saldo:,}'
                        saldotampil = saldotampil.replace(',','.')
                        nominaltampil = f'{nominal:,}'
                        nominaltampil = nominaltampil.replace(',','.')
                        self.lblSaldo.destroy()
                        self.lblSaldo = Label(self, text=f'Saldo anda saat ini\t: Rp {saldotampil},-', style='TLabel')
                        self.lblSaldo.grid(row=5, column=0, columnspan=4, padx=8, sticky='w')
                        messagebox.showinfo('Berhasil', f'Penarikan sebesar Rp {nominaltampil},- telah berhasil')
                    else :
                        messagebox.showerror('Kesalahan', 'Nominal penarikan wajib kelipatan Rp 50.000,-')
                else :
                    messagebox.showerror('Kesalahan', 'Saldo tidak cukup')
            else :
                messagebox.showerror('Kesalahan', 'PIN Salah')
        else :
            messagebox.showerror('Kesalahan', 'Terdeteksi form kosong')

    def Menu(self):
        self.destroy()
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        libs = WindowMenu(*data)
        libs.mainloop()

    def Keluar(self):
        messagebox.showinfo('Terima Kasih', 'Terima kasih telah menggunakan SmartBank UDINUS\nSemoga hari anda menyenangkan')
        self.destroy()

class WindowStatus(Tk):
    def __init__(self, data):
        super().__init__()
        
        self.nama = data[0]
        self.nim = data[1]
        self.pin = data[2]
        self.saldo = data[3]
        statusmember = ''
        bungapertahun = 0
        if self.saldo > 10000000 :
            if self.saldo > 50000000 :
                if self.saldo > 100000000 :
                    if self.saldo > 500000000 :
                        statusmember = 'Diamond' #10%
                        bungapertahun = 0.1
                        bungatampil = '10%'
                    else :
                        statusmember = 'Platinum' #7%
                        bungapertahun = 0.07
                        bungatampil = '7%'
                else :
                    statusmember = 'Gold' #4%
                    bungapertahun = 0.04
                    bungatampil = '4%'
            else :
                statusmember = 'Silver' #1%
                bungapertahun = 0.01
                bungatampil = '1%'
        else :
            statusmember = 'Klasik' #0%
            bungapertahun = 0
            bungatampil = '0%'

        bunga_akhir = int(self.saldo*bungapertahun)
        bunga_akhir = f'{bunga_akhir:,}'
        bunga_akhir = bunga_akhir.replace(',','.')

        saldotampil = f'{self.saldo:,}'
        saldotampil = saldotampil.replace(',','.')

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('447x515')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Status Keanggotaan', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=0, column=0, padx=8, pady=15) 

        self.lblJudul = Label(self, text=f'Saldo anda Rp {saldotampil},-', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=1, column=0, padx=8, sticky='w')

        self.lblJudul = Label(self, text=f'Status Keanggotaan : {statusmember}', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=2, column=0, padx=8, sticky='w')

        self.lblJudul = Label(self, text=f'1.  Diamond\n     Saldo minimal\t: Rp 500.000.000,-\n     Bunga per tahun\t: 10%', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=3, column=0, padx=8, pady=(10,3), sticky='w')

        self.lblJudul = Label(self, text=f'2.  Platinum\n     Saldo minimal\t: Rp 100.000.000,-\n     Bunga per tahun\t: 7%', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=4, column=0, padx=8, pady=3, sticky='w')

        self.lblJudul = Label(self, text=f'3.  Gold\n     Saldo minimal\t: Rp 50.000.000,-\n     Bunga per tahun\t: 4%', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=5, column=0, padx=8, pady=3, sticky='w')

        self.lblJudul = Label(self, text=f'4.  Silver\n     Saldo minimal\t: Rp 10.000.000,-\n     Bunga per tahun\t: 1%', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=6, column=0, padx=8, pady=3, sticky='w')

        self.lblJudul = Label(self, text=f'5.  Klasik\n     Saldo minimal\t: Rp 0,-\n     Bunga per tahun\t: 0%', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=7, column=0, padx=8, pady=3, sticky='w')

        self.lblJudul = Label(self, text=f'Perkiraan Bunga yang akan anda peroleh tahun ini adalah {bungatampil}\nSebesar Rp {bunga_akhir},-', style='TLabel', font=('Helvetica', 12))
        self.lblJudul.grid(row=8, column=0, padx=8, pady=3, sticky='w')

        #deklarasi button
        self.buttonKembali = Button(self, text='Menu', style='TButton', command=self.Menu)
        self.buttonKembali.grid(row=9, column=0, padx=8, pady=10, sticky='w')

        self.buttonKeluar = Button(self, text='Keluar', style='TButton', command=self.Keluar)
        self.buttonKeluar.grid(row=9, column=0, columnspan=3, padx=8, pady=10, sticky='e')

    def Menu(self):
        self.destroy()
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        libs = WindowMenu(*data)
        libs.mainloop()

    def Keluar(self):
        messagebox.showinfo('Terima Kasih', 'Terima kasih telah menggunakan SmartBank UDINUS\nSemoga hari anda menyenangkan')
        self.destroy()

class WindowTransferSaldo(Tk):
    def __init__(self, data):
        super().__init__()
        
        self.nama = data[0]
        self.nim = data[1]
        self.pin = data[2]
        self.saldo = data[3]
        saldotampil = f'{self.saldo:,}'
        saldotampil = saldotampil.replace(',','.')

        #deklarasi windows
        self.title('SmartBank UDINUS')
        self.geometry('332x216')
        self.configure(bg='#89d1ff')
        self.resizable(width=False, height=False)
        self.iconbitmap(r'smartbank.ico')

        #deklarasi style
        Style().configure('TLabel', foreground='black', background='#89d1ff') 
        Style().configure('TButton', foreground='black', background='black')

        #deklarasi label
        self.lblJudul = Label(self, text='Transfer Saldo', style='TLabel', font=('Helvetica', 11))
        self.lblJudul.grid(row=0, column=0, columnspan=4, pady=10) 

        self.lblNominal = Label(self, text='Nominal Transfer\t\t:', style='TLabel')
        self.lblNominal.grid(row=1, column=0, padx=8, sticky='w')

        self.labelRupiah = Label(self, text='Rp', style='TLabel')
        self.labelRupiah.grid(row=1, column=1, sticky='w')

        self.labelSatuan = Label(self, text=',-', style='TLabel')
        self.labelSatuan.grid(row=1, column=3, sticky='w')
    
        self.lblPenerima = Label(self, text='Rekening NIM Penerima\t:', style='TLabel')
        self.lblPenerima.grid(row=2, column=0, padx=8, sticky='w')

        self.lblPINKonfirmasi = Label(self, text='Konfirmasi PIN Anda\t:', style='TLabel')
        self.lblPINKonfirmasi.grid(row=3, column=0, padx=8, sticky='w')

        #deklarasi entry
        self.entryNominal = Entry(self)
        self.entryNominal.grid(row=1, column=2, sticky='w', pady=3)

        self.entryPenerima = Entry(self)
        self.entryPenerima.grid(row=2, column=2, sticky='w', pady=3)

        self.entryPINKonfirmasi = Entry(self, show='*')
        self.entryPINKonfirmasi.grid(row=3, column=2, columnspan=3, sticky='w', pady=3)

        #deklarasi button
        self.buttonTransferSaldo = Button(self, text='Transfer Saldo', style='TButton', command=self.TransferSaldo)
        self.buttonTransferSaldo.grid(row=4, column=0, columnspan=4, pady=5)

        self.buttonKembali = Button(self, text='Menu', style='TButton', command=self.Menu)
        self.buttonKembali.grid(row=5, column=0, padx=8, pady=5, sticky='w')

        self.buttonKeluar = Button(self, text='Keluar', style='TButton', command=self.Keluar)
        self.buttonKeluar.grid(row=5, column=2, columnspan=3, pady=5, sticky='e')

        self.lblSaldo = Label(self, text=f'Saldo anda saat ini\t: Rp {saldotampil},-', style='TLabel')
        self.lblSaldo.grid(row=6, column=0, columnspan=4, padx=8, sticky='w')
    
    def TransferSaldo(self):
        if self.entryNominal.get() != '' and self.entryPenerima.get() != '' and self.entryPINKonfirmasi.get() != '' :
            nominal = f'{self.entryNominal.get()}'
            if '.' in nominal :
                if ',' in nominal :
                    nominal = nominal.replace('.','')
                    nominal = nominal.replace(',','')
                    nominal = eval(nominal)  
                else :
                    nominal = nominal.replace('.','')
                    nominal = eval(nominal)  
            elif ',' in nominal :
                if '.' in nominal :
                    nominal = nominal.replace(',','')
                    nominal = nominal.replace('.','')
                    nominal = eval(nominal)  
                else :
                    nominal = nominal.replace(',','')
                    nominal = eval(nominal)  
            else :
                nominal = eval(nominal)
            rekPenerima = f'{self.entryPenerima.get().capitalize()}'
            query = f'select Nama from users where NIM="{rekPenerima}"'
            cekPenerima = select(query)
            namaPenerima = f'{cekPenerima[0]}'
            namaPenerima = namaPenerima.replace('(','')
            namaPenerima = namaPenerima.replace(')','')
            namaPenerima = namaPenerima.replace("'",'')
            namaPenerima = namaPenerima.replace('"','')
            namaPenerima = namaPenerima.replace(',','')
            if self.entryPINKonfirmasi.get() == self.pin :
                if nominal <= self.saldo :
                    if cekPenerima :
                        self.saldo -= nominal
                        update(-nominal, self.nim)
                        update(+nominal, rekPenerima)
                        self.entryNominal.delete(0,'end')
                        self.entryPINKonfirmasi.delete(0,'end')
                        self.entryPenerima.delete(0,'end')
                        saldotampil = f'{self.saldo:,}'
                        saldotampil = saldotampil.replace(',','.')
                        nominaltampil = f'{nominal:,}'
                        nominaltampil = nominaltampil.replace(',','.')
                        self.lblSaldo.destroy()
                        self.lblSaldo = Label(self, text=f'Saldo anda saat ini\t: Rp {saldotampil},-', style='TLabel')
                        self.lblSaldo.grid(row=6, column=0, columnspan=4, padx=8, sticky='w')
                        messagebox.showinfo('Berhasil', f'Transfer sebesar Rp {nominaltampil},- ke rekening {rekPenerima} a.n {namaPenerima} telah berhasil')
                    else :
                        messagebox.showerror('Kesalahan', 'Rekening NIM penerima tidak terdaftar')
                else :
                    messagebox.showerror('Kesalahan', 'Saldo tidak cukup')
            else :
                messagebox.showerror('Kesalahan', 'PIN Salah')
        else :
            messagebox.showerror('Kesalahan', 'Terdeteksi form kosong')

    def Menu(self):
        self.destroy()
        data = [(self.nama,self.nim,self.pin,self.saldo)]
        libs = WindowMenu(*data)
        libs.mainloop()

    def Keluar(self):
        messagebox.showinfo('Terima Kasih', 'Terima kasih telah menggunakan SmartBank UDINUS\nSemoga hari anda menyenangkan')
        self.destroy()

if __name__ == '__main__' :
    app = WindowLogin()
    app.mainloop()