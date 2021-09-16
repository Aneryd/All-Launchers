from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import os
import sqlite3
from pywinauto.application import Application
import time
# from ttkthemes import ThemedTk, THEMES
from pystray import MenuItem as item
import pystray

root = Tk()
root.iconphoto(True, PhotoImage(file='small_wayder.png'))
# root.config(bg="#2B2B2B")
# root = ThemedTk(themebg=True)
root.title("ALL_LAUNCHERS")
root.geometry('640x480')
# root.set_theme("black")

global field_title, field_img, field, launcher_frame, id_data, field_cashe, field_data, launcher_title, login, password, cb, login_title, password_title, game_type

photo_cache = []
field_cashe = []
game_type = []
loging = []
passw = []

launcher_frame = LabelFrame(root, text='LAUNCHERS')
# launcher_frame.config(bg='#2B2B2B')
canvas = Canvas(launcher_frame)
lf_scrollbar = Scrollbar(launcher_frame, orient='vertical', command=canvas.yview)
scrollbar_frame = Frame(canvas)
#  width=620

#Database
con = sqlite3.connect('launchers.db')
#Create cursor
c = con.cursor()


#Create table
c.execute("""CREATE TABLE IF NOT EXISTS launchers (
		id integer primary key,
		name text,
		title_launcher text,
		find_image text,
		login text,
		password text,
		game text
		)""")

con.commit()

def update_launcher():
	def update(name_l, field_l, img_l, login_l, password_l):

		if len(name_l.get('1.0', 'end-1c')) != 0:
			n_name = name_l.get('1.0', 'end-1c')
		else:
			n_name = ''

		if len(field_l.get('1.0', 'end-1c')) != 0:
			n_field = field_l.get('1.0', 'end-1c')
		else:
			n_field = ''

		if len(img_l.get('1.0', 'end-1c')) != 0:
			n_img = img_l.get('1.0', 'end-1c')
		else:
			n_img = ''

		if len(login_l.get('1.0', 'end-1c')) != 0:
			n_login = login_l.get('1.0', 'end-1c')
		else:
			n_login = ''

		if len(password_l.get('1.0', 'end-1c')) != 0:
			n_password = password_l.get('1.0', 'end-1c')
		else:
			n_password = ''
		#Database
		con = sqlite3.connect('launchers.db')
		#Create cursor
		c = con.cursor()

		for selected_item in tree.selection():
			c.execute("""UPDATE launchers SET name == (?) WHERE id == (?)""", (n_name, tree.set(selected_item, '#1'),))
			c.execute("""UPDATE launchers SET title_launcher == (?) WHERE id == (?)""", (n_field, tree.set(selected_item, '#1'),))
			c.execute("""UPDATE launchers SET find_image == (?) WHERE id == (?)""", (n_img, tree.set(selected_item, '#1'),))
			c.execute("""UPDATE launchers SET login == (?) WHERE id == (?)""", (n_login, tree.set(selected_item, '#1'),))
			c.execute("""UPDATE launchers SET password == (?) WHERE id == (?)""", (n_password, tree.set(selected_item, '#1'),))
			#Commit changes
			con.commit()
			# tree.delete(selected_item)

		#Close Connection
		con.close()

	upt = Toplevel()
	# upt.config(bg="#2B2B2B")
	# upt = ThemedTk()
	upt.title("delete")
	upt.geometry('700x400')
	upt.grab_set()
	# upt.set_theme("black")

	#Database
	con = sqlite3.connect('launchers.db')
	#Create cursor
	c = con.cursor()

	# fr = Frame(dell)
	# fr.pack(expand=1, anchor=NW, padx=0, pady=0)

	columns = ('#1', '#2', '#3', '#4', '#5', '#6')
	tree = ttk.Treeview(upt, show="headings", columns=columns)
	tree.heading('#1', text="id")
	tree.heading('#2', text='Имя')
	tree.heading('#3', text='Путь до лаунчера')
	tree.heading('#4', text='Путь до иконки')
	tree.heading('#5', text='Логин')
	tree.heading('#6', text='Пароль')
	tree.column("#1", width=40)
	tree.column("#2", width=60)
	tree.column("#3", width=290)
	tree.column("#4", width=200)
	tree.column("#5", width=80)
	tree.column("#6", width=80)
	tree.config(height=4)
	tsb = ttk.Scrollbar(upt, orient=VERTICAL, command=tree.yview)
	tree.configure(yscroll=tsb.set)
	# tree.configure(width=390, height=150)
	tree.grid(row=0, column=0)


	button = Button(upt, width=20, height=5, text='edit', command=lambda: update(name_title, title_t, img_titel, lg_titel, pas_titel))
	button.grid(row=1, column=0)

	# print(tree.selection())


	name_label = Label(upt, text='Имя')
	name_title = Text(upt, width=30, height=2)

	title_label = Label(upt, text='Путь до приложения')
	title_t = Text(upt, width=30, height=2)

	img_label = Label(upt, text="Путь до иконки")
	img_titel = Text(upt, width=30, height=2)

	lg_label = Label(upt, text="Логин")
	lg_titel = Text(upt, width=30, height=2)


	pas_label = Label(upt, text="Пароль")
	pas_titel = Text(upt, width=30, height=2)


	name_label.grid_remove()
	name_title.grid_remove()
	title_label.grid_remove()
	title_t.grid_remove()
	img_label.grid_remove()
	img_titel.grid_remove()
	lg_label.grid_remove()
	lg_titel.grid_remove()
	pas_label.grid_remove()
	pas_titel.grid_remove()

	data = []
	di = []
	name_data = []
	img_data = []
	lg_data = []
	pas_data = []

	id_data = c.execute("""SELECT id FROM launchers""").fetchall()
	i = 0
	while i in range(len(id_data)):
		di.append(c.execute("""SELECT id FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		name_data.append(c.execute("""SELECT name FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		data.append(c.execute("""SELECT title_launcher FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		img_data.append(c.execute("""SELECT find_image FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		lg_data.append(c.execute("""SELECT login FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		pas_data.append(c.execute("""SELECT password FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		tree.insert("", 0, values=(di[i], name_data[i], data[i], img_data[i], lg_data[i], pas_data[i]))
		i += 1

	# for selected_item in tree.selection():
	# 	print(tree.set(selected_item, '#1'))

	def on_select(event):
		# print(tree.selection()[0])
		name_label.grid(row=2, column=0)
		name_title.grid(row=2, column=1)
		title_label.grid(row=3, column=0)
		title_t.grid(row=3, column=1)
		img_label.grid(row=4, column=0)
		img_titel.grid(row=4, column=1)
		lg_label.grid(row=5, column=0)
		lg_titel.grid(row=5, column=1)
		pas_label.grid(row=6, column=0)
		pas_titel.grid(row=6, column=1)

		name_title.delete('1.0', 'end')
		title_t.delete('1.0', 'end')
		img_titel.delete('1.0', 'end')
		lg_titel.delete('1.0', 'end')
		pas_titel.delete('1.0', 'end')

		for selected_item in tree.selection():
			name = tree.set(selected_item, '#2')
			title = tree.set(selected_item, '#3')
			img = tree.set(selected_item, '#4')
			lg = tree.set(selected_item, '#5')
			pasw = tree.set(selected_item, '#6')

		name_title.insert('1.0', name)
		title_t.insert('1.0', title)
		img_titel.insert('1.0', img)
		lg_titel.insert('1.0', lg)
		pas_titel.insert('1.0', pasw)

	tree.bind('<<TreeviewSelect>>', on_select)

	#Commit changes
	con.commit()
	#Close Connection
	con.close()

	upt.mainloop()

def select_db():
	def open_launcher(find, game, log, passwor):
		if game == 'lol':
			app = Application(backend='uia').start(r"{}".format(find))
			app = Application(backend='uia').connect(title="Riot Client", timeout=60)

			app.RiotClient.Edit1.click_input()
			app.RiotClient[u'Edit1:Edit'].type_keys(str(log), with_spaces=True, set_foreground=False)

			app.RiotClient.Edit2.click_input()
			app.RiotClient[u'Edit2:Edit'].type_keys(str(passwor), with_spaces=True, set_foreground=False)

			app.RiotClient.Button5.click_input()
		else:
			app = Application(backend='uia').start(find)

	#Database
	con = sqlite3.connect('launchers.db')
	#Create cursor
	c = con.cursor()

	id_data = c.execute("""SELECT id FROM launchers""").fetchall()
	# print(id_data[0][0])
	i = 0
	rw = 1
	clm = 1
	while i in range(len(id_data)):
		name_launcher = c.execute("""SELECT name FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone()
		field_data = c.execute("""SELECT title_launcher FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone()
		file_img = c.execute("""SELECT find_image FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone()
		login = c.execute("""SELECT login FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone()
		password = c.execute("""SELECT password FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone()
		game = c.execute("""SELECT game FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone()

		#Добавление ссылки на приложение в массив
		# if (field_data and file_img) is not None:
		field_cashe.append(field_data[0])

		game_type.append(game[0])

		loging.append(login[0])
		passw.append(password[0])

		#Обработка изображения и добавление его в массив
		photo = PhotoImage(file=file_img)
		photo1 = photo.subsample(10, 10)
		photo_cache.append(photo1)
	
		# global auto_button_launcher
		# launcher_frame.pack(expand=1, anchor=NW)
		# launcher_frame.pack_propagate(0)
		global auto_button_launcher
		launcher_frame.grid(row=0, column=0)
		auto_button_launcher = Button(launcher_frame, width=200, height=200, image=photo_cache[-1], text=name_launcher, compound='top', command=lambda fl=field_cashe[-1], gm=game_type[-1], lg=loging[-1], ps=passw[-1]: open_launcher(fl, gm, lg, ps))
		# auto_button_launcher.pack(expand=1, side=LEFT)
		auto_button_launcher.grid(row=rw, column=clm)

		if clm % 3 == 0:
			rw += 1
			clm= 0

		clm += 1
		i += 1

	con.commit()
	#Close Connection
	con.close()

if os.path.isfile('launchers.db') == True:
	select_db()

def delete_launchers():
	def delete():		
		#Database
		con = sqlite3.connect('launchers.db')
		#Create cursor
		c = con.cursor()

		for selected_item in tree.selection():
			c.execute("""DELETE FROM launchers WHERE id == (?)""", (tree.set(selected_item, '#1'),))
			#Commit changes
			con.commit()
			tree.delete(selected_item)
			# вроде удаление кнопки
			# auto_button_launcher.pack_forget(selected_item)

			# auto_button_launcher.pack_forget(selected_item)

		#Close Connection
		con.close()

	dell = Toplevel()
	dell.title("delete")
	dell.geometry('398x200')
	dell.grab_set()

	#Database
	con = sqlite3.connect('launchers.db')
	#Create cursor
	c = con.cursor()

	# fr = Frame(dell)
	# fr.pack(expand=1, anchor=NW, padx=0, pady=0)

	columns = ('#1', '#2')
	tree = ttk.Treeview(dell, show="headings", columns=columns)
	tree.heading('#1', text="id")
	tree.heading('#2', text='Путь')
	tree.column("#1", width=40)
	tree.column("#2", width=350)
	tree.config(height=4)
	tsb = ttk.Scrollbar(dell, orient=VERTICAL, command=tree.yview)
	tree.configure(yscroll=tsb.set)
	# tree.configure(width=390, height=150)
	tree.grid(row=0, column=0)


	button = Button(dell, width=20, height=5, text='delete', command=lambda: delete())
	button.grid(row=1, column=0)


	data = []
	di = []

	id_data = c.execute("""SELECT id FROM launchers""").fetchall()
	i = 0
	while i in range(len(id_data)):
		di.append(c.execute("""SELECT id FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		data.append(c.execute("""SELECT title_launcher FROM launchers WHERE id == (?)""", (id_data[i][0],)).fetchone())
		tree.insert("", 0, values=(di[i], data[i]))
		i += 1


	#Commit changes
	con.commit()
	#Close Connection
	con.close()

	dell.mainloop()

def setting():
	sett = Toplevel()
	sett.title("settings")
	sett.geometry('398x200')
	sett.grab_set()

	#Кнопка выбора пути
	def field_launcher():
		ft = filedialog.askopenfilename(title='Укажите путь до лаунчера', filetypes=[("EXE", "*.exe")])
		field_title.delete('1.0', 'end')
		field_title.insert('1.0', ft)

	#Кнопка выбора изображения
	def fl_img():
		fi = filedialog.askopenfilename(title='Укажите путь до изображения', filetypes=[("IMAGE", "*.png; *.jpg")])
		field_img.delete('1.0', 'end')
		field_img.insert('1.0', fi)

	def add_launcher():
		def open():
			if cb.get() == True:
				app = Application(backend='uia').start(field)
				app = Application(backend='uia').connect(title="Riot Client", timeout=60)

				app.RiotClient.Edit1.click_input()
				app.RiotClient[u'Edit1:Edit'].type_keys(str(login), with_spaces=True, set_foreground=False)

				app.RiotClient.Edit2.click_input()
				app.RiotClient[u'Edit2:Edit'].type_keys(str(password), with_spaces=True, set_foreground=False)

				app.RiotClient.Button5.click_input()
			else:	
				app = Application(backend='uia').start(field)
		
		field = field_title.get('1.0', 'end-1c')
		img = field_img.get('1.0', 'end-1c')
		name_launcher = launcher_title.get('1.0', 'end-1c')

		if cb.get() == True:
			login = login_title.get('1.0', 'end-1c')
			password = password_title.get('1.0', 'end-1c')
			game = 'lol'
		else:
			login = ''
			password =''
			game =''

		photo = PhotoImage(file=img)
		photo1 = photo.subsample(10, 10)
		photo_cache.append(photo1)

		# launcher_frame.pack(expand=1, anchor=NW)
		# launcher_frame.pack_propagate(0)
		launcher_frame.grid(row=0, column=0)
		button_launcher = Button(launcher_frame, width=200, height=200, image=photo_cache[-1], text=name_launcher, compound='top', command=lambda: open())
		# button_launcher.pack(side=LEFT)
		widjet = auto_button_launcher.grid_info()
		clm = widjet['column']
		rw = widjet['row']
		if clm % 3 == 0:
			rw += 1
			clm = 0
		else:
			clm += 1
		button_launcher.grid(row=rw, column=clm)

		#Database
		con = sqlite3.connect('launchers.db')
		#Create cursor
		c = con.cursor()
		c.execute(""" INSERT INTO launchers (name, title_launcher, find_image, login, password, game) VALUES (?, ?, ?, ?, ?, ?);""", (name_launcher, field, img, login, password, game))
		#Commit changes
		con.commit()
		#Close Connection
		con.close()

	# Название лаунчера
	label_name = Label(sett, text='Название лаунчера')
	launcher_title = Text(sett, width=30, height=2)
	label_name.grid(row=0, column=0)
	launcher_title.grid(row=0, column=1)

	#Лаунчер
	label_title = Label(sett, text='Путь до приложения')
	field_title = Text(sett, width=30, height=2)
	#Создание кнопки выбора пути
	button_title = Button(sett, width=2, height=2, text='+', command=lambda: field_launcher())

	label_title.grid(row=1, column=0)
	field_title.grid(row=1, column=1)
	button_title.grid(row=1, column=2)

	#Изображение
	label_img = Label(sett, text='Путь до изображения')
	field_img = Text(sett, width=30, height=2)
	#Создание кнопки выбора картинки
	button_img = Button(sett, width=2, height=2, text='+', command=lambda: fl_img())

	label_img.grid(row=2, column=0)
	field_img.grid(row=2, column=1)
	button_img.grid(row=2, column=2)

	#Кнопка добавления лаунчера
	button_add = Button(sett, width=20, height=2, text='add', command=lambda: add_launcher())
	button_add.grid(row=3, column=0)

	#Checkbox выбора lol
	cb = BooleanVar()
	cb.set(0)
	cb_lol = Checkbutton(sett, variable=cb, text='lol', onvalue=1, offvalue=0)
	cb_lol.grid(row=4, column=0)


	login_label = Label(sett, text='login')
	login_title = Text(sett, width=30, height=2)
	login_label.grid(row=5, column=0)
	login_title.grid(row=5, column=1)

	password_label = Label(sett, text='password')
	password_title = Text(sett, width=30, height=2)
	password_label.grid(row=6, column=0)
	password_title.grid(row=6, column=1)

	sett.mainloop()

#Создание меню
menu = Menu(root)
root.config(menu=menu)

new_item = Menu(menu)
menu.add_cascade(label='settings', menu=new_item)
new_item.add_command(label='add launcher', command=lambda: setting())
new_item.add_command(label='delete launcher', command=lambda: delete_launchers())
new_item.add_command(label='edit launcher', command=lambda: update_launcher())

#3 функции которые управляют иконкой в трее
def quit_window():
    icon.stop()
    root.destroy()

def show_window():
    icon.stop()
    root.after(0, root.deiconify)

def withdraw_window():  
    root.withdraw()
    image = Image.open("small_wayder.png")
    menu = (item('Quit', lambda: quit_window()), item('Show', lambda: show_window()))
    global icon
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()

root.protocol('WM_DELETE_WINDOW', lambda: withdraw_window())

root.mainloop()