from tkinter import *
import random

colour_mother   = '#%02x%02x%02x' % (105,153,97)
colour_analysis = '#%02x%02x%02x' % (244,237,119)
colour_way_points = '#%02x%02x%02x' % (244,237,119)
colour_aspect_good = '#254280'
colour_aspect_bad = '#AD1111'

list_figures = (
  ('Puer', '1211', ['Mars']), 
  ('Puella', '1121', ['Wenus']),
  ('Amissio', '2121', ['Wenus']),            
  ('Acquisitio', '1212', ['Jowisz']),
  ('Albus', '2122', ['Merkury']),              
  ('Rubeus', '2212', ['Mars']),
  ('Populus', '2222', ['Księżyc']),            
  ('Via', '1111', ['Księżyc']),
#  ('Fortuna Major', '1122'),      
  ('F. Major', '1122', ['Sun']),        
#  ('Fortuna Minor', '2211'),
  ('F. Minor', '2211', ['Słońce']),
  ('Conjunctio', '2112', ['Merkury']),         
  ('Carcer', '1221', ['Saturn']),
  ('Tristitia', '1222', ['Saturn']),          
  ('Laetitia', '2221', ['Jowisz']),
#  ('Caput Draconis', '1112'),
#  ('Cauda Draconis', '2111'),     
  ('Cauda Dracon.', '2111', ['Mars', 'Saturn']),      
  ('Caput Dracon.', '1112', ['Wenus', 'Jowisz'])
) 

list_compound = ( ('Puer', 'Puella'), ('Amissio', 'Acquisitio'),
  ('Albus', 'Rubeus'), ('Populus', 'Via'),
  ('F. Major', 'F. Minor'), ('Conjunctio', 'Carcer'),
  ('Tristitia', 'Laetitia'), ('Cauda Dracon.', 'Caput Dracon.')
)

judges = { # lewy - prawy - dom
  '2222': {'2222': {1: 'Mod.', 2: 'Mod.', 3: 'Mod.', 4: 'Mod.', 5: 'Good', 6: '5', 7: 'Asc.', 8: 'Come out', 9: 'Good by water', 10: 'Found'}  }
}

lista_aspects = []
lista_comp_planets = []

list_houses = (' 2. Pieniądze, ruchomości. Zyski i straty.',
               ' 3. Rodzeństwo, otoczenie, wiadomości, krótkie podróże, szkoła.',
               ' 4. Ziemia, budynki, zmiany miejsca, ojciec, rzeczy ukryte, koniec.',
               ' 5. Plony, ciąża, dzieci, płciowość. Zabawa, jedzenie i picie, woda.',
               ' 6. Podwładni, usługodawcy, okultyści, zwierzęta domowe, choroby, rany.',
               ' 7. Miłość, małżeństwo, partnerstwo, konkurencja, wrogowie, osoby szukane.',
               ' 8. Śmierć, duchy, praktyki magiczne kwerenta. Nieobecność, zaginięcie, pożyczka.',
               ' 9. Dalekie podróże, religia i duchowość, wyższa edukacja, własne praktyki okultystyczne.',
               '10. Pozycja zawodowa i społeczna, kariera, osoby sprawujące władzę, matka, polityka, stan pogody.',
               '11. Przyjaciele, sojusznicy, źródła pomocy, plany i nadzieje.',
               '12. Ograniczenia, przeszkody, długi, więzienie, tajemnice, rzeczy nieznane.')


class Modes_Perfection:
  def __init__ (self, button, odpowiedzi, opis, function):
    self.pressed = False
    self.function = function
    self.button = button
    self.odpowiedzi = odpowiedzi
    self.opis = opis
    self.button.configure(text = opis, command = lambda: self.myfunction() )
    
  def myfunction(self):
    for i in houses: houses[i].clear_colour()
    draw_aspects_clear()
    draw_comp_planets_clear()
    houses[1].change_colour('gray')
    houses[quesited].change_colour('gray')
    for i in modes_perfection.keys(): 
      if modes_perfection[i].opis != self.opis: 
        modes_perfection[i].pressed = False
    if self.pressed:
      self.pressed = False
    else:
      self.paint_houses( self.do_function() )
      self.pressed = True
  def do_function(self):
    p = self.function()
    self.odpowiedzi.configure(text = len(p))
    if (p): self.button.configure(state = 'normal')
    else: self.button.configure(state = 'disabled')
    return p
  def paint_houses (self,tables):
#    colour = ('red', 'blue', 'green', 'yellow', 'magenta', 'gray')
    colour = ('#9b111e', '#8bb9dd', '#a9d171', '#cca978', '#f6c9aa', '#b5b5b5')
    nr = 0
    for table in tables:
      houses[ table[0] ].change_colour(colour_way_points)
      houses[ table[1] ].change_colour(colour_way_points)
      houses[ table[0] ].ramka_show(nr,colour[nr])
      houses[ table[1] ].ramka_show(nr,colour[nr])
      nr += 1
    houses[1].change_colour('gray')
    houses[quesited].change_colour('gray')
    
class House:
  def __init__ (self, canv, x,y, bok, rodzaj, nr):
    x2 = x; y2 = y;  x3 = x;  y3 = y
    outline_color = 'black'
    font_figura = 'Symbol 12'
    font_text = 12
    if str(nr)[0] == 'W' or str(nr)[0] == 'J':
      nr = ''
      outline_color= ''
#      font_figura = 'Symbol 10'
#      font_text = 'Times 8'

    self.srodek = [x,y]
    self.coloured = '' # kolor lub puste dla ''
    self.id = -1
    self.planet = ''
    self.canv = canv
    self.rodzaj = rodzaj
    self.txt = '1211'
    self.ramki = []
    self.nr_domu = canv.create_text(x, y, text = nr, font = font_text)
    self.figura = canv.create_text(x, y, font = font_figura, text = read_figura(self.txt), 
        justify='center')
    if rodzaj == 'l':
      y2 += bok
      x3 += (bok/2)
      y3 += (bok/2)
      self.srodek[0] += bok/4
      self.srodek[1] += bok/2
      canv.coords(self.nr_domu, x + bok/2.5, y + bok/2)
      canv.coords(self.figura, x + bok/6, y + bok/2)
    
    if rodzaj == 'r': # kreska pozioma z prawej strony
      y2 += bok
      x3 -= (bok/2)
      y3 += (bok/2)
      self.srodek[0] -= bok/4
      self.srodek[1] += bok/2
      canv.coords(self.nr_domu, x - bok/2.5, y + bok/2)
      canv.coords(self.figura, x - bok/6, y + bok/2)

    if rodzaj == 'u':
      x2 += bok
      x3 += (bok/2)
      y3 += (bok/2)
      self.srodek[0] += bok/2
      self.srodek[1] += bok/4
      canv.coords(self.nr_domu, x + bok/2, y + bok/2.5)
      canv.coords(self.figura, x + bok/2, y + bok/6)

    if rodzaj == 'd': # kreska pozioma na dole
      x2 += bok
      x3 += (bok/2)
      y3 -= (bok/2)
      self.srodek[0] += bok/2
      self.srodek[1] -= bok/4
      canv.coords(self.nr_domu, x + bok/2, y - bok/2.5)
      canv.coords(self.figura, x + bok/2, y - bok/6)
      
    self.tr = canv.create_polygon(x,y, x2,y2, x3,y3, fill=self.coloured, outline=outline_color, width = 2)
    canv.tag_lower(self.tr) # przeniesienie poniżej innych elementów canvasu
    for i in range(1,40,4):
      self.ramka(i)
    
  def change_colour(self,colour):
    self.canv.itemconfigure(self.tr, fill=colour)
  def get_ramka_colour(self,nr):
    p = self.canv.itemconfigure(self.ramki[nr], 'outline')
    return p[-1]
  def clear_colour(self):
    self.coloured = ''
    self.canv.itemconfigure(self.tr, fill=self.coloured)
    for i in self.ramki:
      self.canv.itemconfigure(i,outline=self.coloured)
  def link_srodki(self, other, colour, size):
    p = canv_houses.create_line(self.srodek, other.srodek, 
           fill = colour, width=size)
    for i in (houses):
      self.canv.tag_raise(houses[i].figura)
      self.canv.tag_raise(houses[i].nr_domu)
    for i in (witness_judge.keys()):
      self.canv.tag_raise(witness_judge[i].figura)
      self.canv.tag_raise(witness_judge[i].nr_domu)
    return p
  def napis_planeta (self, other, planeta):
    x1, y1 = self.srodek
    x2, y2 = other.srodek
    x = x1
    if x1 < x2: x += (x2 - x1) /2
    else: x -= (x1 - x2) /2
    y = y1
    if y1 < y2: y += (y2 - y1) /2
    else: y -= (y1 - y2) /2
    p = canv_houses.create_text(x, y, text = planeta, justify = CENTER, font = "Times 12")
    i = canv_houses.create_rectangle(canv_houses.bbox(p), fill='white', outline="")
    canv_houses.tag_lower(i,p)
    for n in (self, other):
      self.canv.tag_raise(n.figura)
#      self.canv.tag_raise(n.nr_domu)
    return p, i

  def get_id(self,id):
    self.id = id # id figury, np. 1, 15...
    self.txt = list_figures[self.id][1] # '1121'...
    self.name  = list_figures[self.id][0] # 'Puer'...
    self.planet = list_figures[self.id][2] # 'Jupiter'...
    self.canv.itemconfigure(self.figura,text=read_figura(self.txt))
  def get_text(self):
     if self.id < 0: return ''
     return list_figures[self.id][1]
  def ramka_show(self,n,colour):
    self.canv.itemconfigure(self.ramki[n],outline=colour)
  def ramka(self,size):
    xyz = self.canv.coords(self.tr)
    lista = []
    licznik = 1
    for a in xyz:
      if licznik % 2 == 0:
        if self.srodek[1] > a:
          a += size
          if self.rodzaj in 'rl': a += size
        elif self.srodek[1] < a:
          a -= size
          if self.rodzaj in 'rl': a -=size
      else:
        if self.srodek[0] > a:
          a += size
          if self.rodzaj in 'du': a +=size
        elif self.srodek[0] < a:
          a -= size
          if self.rodzaj in 'du': a -= size
      lista += [a]
      licznik += 1
    p = self.canv.create_polygon(lista,fill='', outline = '', width=4)
    self.canv.tag_raise(p)
    self.canv.tag_raise(self.figura)
    self.canv.tag_raise(self.nr_domu)
    self.ramki.append(p)
    
class Shield:
  def __init__ (self,nr,canv,x1,y1, x2,y2, kind_of='', start=0, extent=0, judges=''):
    self.rectang = ''
    self.text = ''
    self.canv = canv
    self.tr = '' # jak w House; rysowana figura: arc lub prostokąt
    self.id = -1 # numer figury, np. Puer
    self.nr = nr # numer obiektu w tablicy obiektów, np. 12 w shields[12]
    self.coloured = '' # kolor lub puste dla ''
    h = y2-y1; 
    if kind_of != 'arch':
      if kind_of == 'double':
        x2 += x2-x1
      h_width = (x2-x1)/2
      self.tr = canv.create_rectangle(x1,y1, x2,y2, )
      self.text = canv.create_text( x1 + h_width, y1 + h/2, font = "Symbol 12", 
        justify='center')
    else:
      h_width = (x2-x1)/2
      xy = x1, y1, x2, y2
      self.tr = canv.create_arc(*xy, start=start, extent=extent, fill='')
      if judges == 'judge':
        xy = x1 + (x2-x1)/2, y1 + h - h/4
      if judges == 'right':
        xy = x2 - (x2-x1)/4, y1 + h  - h/3
      if judges == 'left':
        xy = x1 + (x2-x1)/4 , y1 + h - h/3
      self.text = canv.create_text(*xy, font = "Symbol 12", 
         justify='center')
    self.modify_text(''),
  def modify_text(self, figura):
    self.id = find_id(figura)
    self.canv.itemconfigure(self.text, text = read_figura(figura))
    self.canv.update()
  def modify_id(self,id): # identyfikator, czyli pozycja na liście, obliczona na zewnątrz
    self.id = id
    self.canv.itemconfigure(self.text, 
      text = read_figura(list_figures[self.id][1]) )
  def get_text(self):
     if self.id < 0: return ''
     return list_figures[self.id][1]
  def change_colour(self,colour):
    if self.coloured == '': self.coloured = colour
    else: self.coloured = ''
    self.canv.itemconfigure(self.tr, fill=self.coloured)

    
def find_id (figura):
  nr = 0
  for (i, j, k) in list_figures:
    if j == figura:
      return nr
    nr += 1
  return -1

def string_reverse(text):
  r = ''
  while text:
    r += text[-1]
    text = text[:-1]
  return r
  
class Mothers:
  def __init__(self, lista):
    self.lista = lista
    self.entry = ''
    self.id = -1 # odpowiada elementowi listy list_figures
  def fill_names(self):
    for name, numer, planet in list_figures:
      self.lista.insert(END,' ' + self.read_figura(numer) + ' ' + name)
  def read_figura (self,tekst):
    r = ''
    for c in tekst:
      if c == '1': r += '\u2027'
      else: r += '\u205A'
    return r
  def chose_entry (self, entry):
    self.entry = entry
    self.lista.bind("<Double-Button-1>", 
      lambda event: self.chosen_lista_my())
    self.lista.bind("<Return>", 
      lambda event: self.chosen_lista_my())
  def replace_entry(self):
    item = self.lista.get(self.id)
    self.entry.delete('1.0',END)
    self.entry.insert(END,item)
  def chosen_lista_my(self):
    self.id = chosen_lista(self.lista,self.entry)
    wypisywanie()
  def clear(self):
    self.id = -1
    self.entry.delete('1.0',END)
    self.lista.selection_clear(0,END)
    chosen_lista(self.lista,self.entry)
    self.lista.see(0)
  def losowane(self):
    self.id = random.randint(0,len(list_figures)-1)
    self.lista.selection_clear(0,END)
    self.lista.selection_set(self.id)  # niebieskie tło
    self.lista.activate(self.id)       # kreska podkreślająca
    self.lista.see(self.id)
    s = self.lista.yview(self.id) # to działa, nie tak jak self.lista.index(self.id)
    chosen_lista(self.lista,self.entry)
    self.replace_entry()
    
def testuj():
  global quesited
  # identyfikator id to numer figury z listy list_figures
  # (odczyt znaku: list_figures[id][1]
  houses[1].change_colour('red')
  houses[quesited].change_colour('yellow')
  for i in houses.keys():
    print (i, houses[i].id, list_figures [ houses[i].id ] [1])
  print ('Quesited:', quesited)


def chosen_lista(list, entry, houses=0):
  global quesited
#  color_bg = 'SystemHighlight'
#  color_fg = 'SystemHighlightText'
  color_bg = '#b1c484'
  color_fg = '#4e3b7b' # opposite to Green Tea
#  list.configure(highlightbackground = color_bg)
#  list.configure(selectbackground = color_bg)
  id = list.curselection()
  if id == (): id = -1
  else: id = id[0]
  for i in range (list.size()):
    if i == id:
      list.itemconfigure(i, bg = color_bg)
      list.itemconfigure(i, fg = color_fg)
    else: 
      list.itemconfigure(i, bg = '')
      list.itemconfigure(i, fg = '')
  if id == (): return
  if id >= 0:
    item = list.get(id)
    entry.delete('1.0',END)
    entry.insert(END,item)
  if houses: # -------------- jeżeli wybór dotyczył domu quesited
    quesited = id + 2 # numer listy, zaczyna się od 2 i jeszcze jest zero
    wypisywanie()
  return id

# Shield.rectang = ''
# Shield.text= ''

def read_figura (tekst):
  r = ''
  for c in (string_reverse(tekst)):
    if c == '1': r += '\u00b7\n'
    else: r += '\u00b7   \u00b7\n'
  return r.strip()

def dodanie_pola (text1, text2):
  r = ''
  for i in range(4):
    n = int (text1[i]) + int (text2[i])
    if n % 2: r += '1'
    else: r += '2'
#  print (r, 'z dodania', text1, text2)
  return r

def houses_configure():
  ho = house_order.get()
  if ho == 'natural':
    for i in range(1,13):
      houses[i].get_id(shields[i].id)
  elif ho == 'GD':
    for i,j in (
      (1,10), (2,1), (3,4), (4,7), # znaki/domy kardynalne
      (5,11), (6,2), (7,5), (8,8), # stałe
      (9,12),  (10,3), (11,6),  (12,9)
     ):
      houses[j].get_id(shields[i].id)
  else: print ('error in houses configure')
  obliczanie_funkcji()

def losowanie():
  global lista_domy
  dom = lista_domy.curselection()
  for i in range(1,5): # od 1 do 4
    mothers[i].losowane()
    shields[i].modify_id(mothers[i].id)
#  dic = 
  wypisywanie()
  for i in houses:
    houses[i].clear_colour()
#  for i in dic.keys():
#    if dic[i]:print ('Znaleziono:', i, ': ', dic[i])
  houses[1].change_colour('gray')
  houses[quesited].change_colour('gray')
  if (dom): lista_domy.selection_set(dom[0])
  else: lista_domy.selection_set(3)
  lista_domy.focus()
  
  
def czyszczenie():
  for i in range(1,5):
    mothers[i].clear()
  for i in range(1,16):
    shields[i].id = -1
    shields[i].modify_text('')
    
def wypisywanie():  
  not_filled = 0
  for i in range(1,5): # od 1 do 4
    if mothers[i].id < 0: 
      not_filled = 1
      continue
    shields[i].modify_id(mothers[i].id)
  if not_filled: return
  nr = 5 # zaczynam od wpisywania w piątym polu
  for i in range (3,-1,-1): # łączenie górnych 1-4 w cztery kolejne córki
    s = shields[4].get_text()[i] + \
        shields[3].get_text()[i] + \
        shields[2].get_text()[i] + \
        shields[1].get_text()[i]
    shields[nr].modify_text(s)
    nr += 1    
  #------------------------------------ nephews or nieces
  shields[9].modify_text  ( dodanie_pola(shields[1].get_text(), shields[2].get_text()) )
  shields[10].modify_text ( dodanie_pola(shields[3].get_text(), shields[4].get_text()) )
  shields[11].modify_text ( dodanie_pola(shields[5].get_text(), shields[6].get_text()) )
  shields[12].modify_text ( dodanie_pola(shields[7].get_text(), shields[8].get_text()) )

  #------------------------------------ świadek prawy, lewy, sędzia
  shields[13].modify_text ( dodanie_pola(shields[9].get_text(), shields[10].get_text()) )
  shields[14].modify_text ( dodanie_pola(shields[11].get_text(), shields[12].get_text()) )
  shields[15].modify_text ( dodanie_pola(shields[13].get_text(), shields[14].get_text()) )
  
  houses_configure()
  witness_judge['r'].get_id(shields[13].id)
  witness_judge['l'].get_id(shields[14].id)
  witness_judge['j'].get_id(shields[15].id)
  # -----------------------------------  sprawdzanie funkcji
  obliczanie_funkcji()
  
def obliczanie_funkcji():
  for i in modes_perfection.keys():
    p = modes_perfection[i].do_function()
  point_index()
  point_index(1)
  draw_aspects_clear()
  draw_comp_planets_clear()
  for i in houses:
    houses[i].clear_colour()
  houses[1].change_colour('gray')
  houses[quesited].change_colour('gray')
  
def canvas_choose_old(side = 'left'):
  canv_show = canv_houses
  canv_hide = canv_shield
  my_side = LEFT
  if side == 'left':
    if var_canvas_left.get() == 'shield':
      (canv_show, canv_hide) = (canv_shield, canv_houses)
  else: # side == 'right'
    canv_show = canv_mothers
    canv_hide = canv_analysis
    my_side = LEFT
    if var_canvas_right.get() == 'analysis':
      (canv_show, canv_hide) = (canv_analysis, canv_mothers)
    if var_canvas_right.get() == 'tests':
      (canv_show, canv_hide) = (canv_tests, canv_mothers)

  canv_show.pack(side=my_side,fill=BOTH,expand=1,anchor='w')
  canv_hide.pack_forget()
#  print (var_canvas_left.get(), var_canvas_right.get())

def canvas_choose (side = 'left'):
  canv_show = canv_houses
  canv_hide = [canv_shield,]
  my_side = LEFT
#  print (side)
  if side == 'left':
    if var_canvas_left.get() == 'shield':
      (canv_show, canv_hide) = (canv_shield, [canv_houses,])
  else: # side == 'right'
    canv_show = canv_mothers
    canv_hide = [canv_analysis, canv_tests]
    my_side = LEFT
    if var_canvas_right.get() == 'analysis':
      canv_show = canv_analysis
      canv_hide = [canv_tests, canv_mothers]
    if var_canvas_right.get() == 'tests':
      canv_show = canv_tests
      canv_hide = canv_analysis, canv_mothers

  canv_show.pack(side=my_side,fill=BOTH,expand=1,anchor='w')
  for i in canv_hide:
     i.pack_forget()
#  print (var_canvas_left.get(), var_canvas_right.get())

def occupation():
  s_qr = houses[1].txt
  s_qs = houses[quesited].txt
  if s_qr == s_qs:
    houses[1].change_colour(colour_way_points)
    houses[quesited].change_colour(colour_way_points)
    return [(1,quesited)]
  return []

def conjunction():
  s_qr = houses[1].txt
  s_qs = houses[quesited].txt
  s_next_to_querent = houses[2].txt # next to the querent
  s_next_to_quesited = ''
  wynik = []
  if (quesited < 12):
    s_next_to_quesited = houses[quesited+1].txt
  if s_next_to_querent == s_qs: # ----------------- koniunkcja z sygnifikatorem kwerenta
    wynik.append( (2,1) )
  if s_next_to_quesited == s_qr: # ---------------- koniunkcja z sygnifikatorem quesited
    wynik.append( (quesited,quesited+1) )
  return wynik
#  nr_qr, nr_qs
   
def mutation():
  s_qr = houses[1].txt
  s_qs = houses[quesited].txt
  s_para = ' '.join( sorted([s_qr, s_qs]) )
  wynik = []
  for i in range(2,12): # od 2 do 11 sprawdzam pary (12 z 1 się nie porównuje)
    si = houses[i].txt
    sj = houses[i+1].txt
    s_wynik = ' '.join( sorted([si, sj]) )
#    print (i, i+1, ':', s_para, '---', s_wynik)
    if s_para == s_wynik:
      if i == quesited or i+1 == quesited: # nie chodzi o połączenie q z sygnifikatorem
                                           # ale o połączenie dwóch sygnifikatorów
        continue # mutacja ale nie coś innego
#      houses[i].change_colour(colour_way_points)
#      houses[i+1].change_colour(colour_way_points)
#      houses[1].change_colour('gray')
#      houses[quesited].change_colour('gray')
#      print ('trafiona para:', i, i+1)
#      r += 1
      wynik.append ( (i,i+1) )
  return wynik
  
def test_funkcji_old():
  n = []
  for i in houses: houses[i].clear_colour()
  nr = 0
  while nr == 0  :
   losowanie()
   n = company_houses()
   nr = len(n)
#   n = aspects()
   '''
   
   n += occupation()
   n += mutation()
   n += conjunction()
   pairs = ( (1,2), (3,4), (5,6), (7,8), (9,10),(11,12))
   for i, j in pairs:
     n = comp_compound (i,j)
     if n: break
  '''
#  print (n)
def test_funkcji():
  for i in houses: houses[i].clear_colour()
  was = 0
  while was == 0:
    losowanie()
    n = 0
    if var_tests_obsadzenie.get():
      if occupation() == []: continue
      else: n += 1
    if var_tests_koniunkcja.get():
      if conjunction() == []: continue
      else: n += 1
    if var_tests_mutacja.get():
      if mutation() == []: continue
      else: n += 1
    if var_tests_translacja.get():
      if translation() == []: continue
      else: n += 1
    if var_tests_aspekty.get():
      if aspects() == []: continue
      else: n += 1
    if var_tests_company_houses.get():
      if company_houses() == []: continue
      else: n += 1
    if var_tests_impedition.get():
      if occupation() != []: continue
      if conjunction() != []: continue
      if mutation() != []: continue
      if translation() != []: continue
#      if aspects() != []: continue
#      if company_houses() != []: continue
    was = 1
  
def translation():
  s_qr = houses[1].txt
  s_qs = houses[quesited].txt
  s_next_qr = houses[2].txt
  if quesited == 12: return [] # nie ma domu po ostatnim
  s_next_qs = houses[quesited+1].txt
  if s_next_qr == s_next_qs and s_next_qr != s_qr: # inna niż sygnifikator
    return [ (1,2), (quesited,quesited+1) ] 
  return []

def draw_aspect(n1, n2, colour, kierunek):
  size_kierunek = 3 # kierunek == 'lewy'
  if kierunek == 'prawy': size_kierunek = 9
  p = houses[n1].link_srodki(houses[n2], colour, size_kierunek)
  lista_aspects.append(p)

def draw_comp_planets(planeta, nr1, nr2): # planeta, dom1, dom2
  p = houses[nr1].napis_planeta(houses[nr2], planeta)
  lista_comp_planets.append( (p,i) )

def add_aspekty(i, j, rodzaj, kierunek):
#  aspekty.add(i)
  aspect_colour = colour_aspect_bad
  if rodzaj in ('sekstyl', 'trygon'):
   aspect_colour = colour_aspect_good
  if rodzaj == 'opozycja': kierunek = 'prawy'
  draw_aspect(i, j, aspect_colour, kierunek)

def draw_aspects_clear():
  global lista_aspects
  for i in lista_aspects:
    canv_houses.delete(i)
  lista_aspects = []

def draw_comp_planets_clear():
  global lista_comp_planets
  for (i, j), k in lista_comp_planets:
    canv_houses.delete(i)
    canv_houses.delete(j)
  lista_comp_planets = []

def aspects():
  global lista_aspects
  s_qr = houses[1].txt
  s_qs = houses[quesited].txt

  draw_aspects_clear()

  signif_qr = []  # lista sygnifikatorów kwerenta, są to numery domów
  signif_qs = []  # lista sygnifikatorów quesited 
  kierunek = ''
  rodzaj = ''
  aspekty = set ()
  wynik = []
  for i in range(1,13):
    s = houses[i].txt
    if s == s_qr and i != 1: signif_qr.append(i)
    if s == s_qs and i != quesited: signif_qs.append(i)
  for i in signif_qr:
    n = i - quesited
    if abs(n) > 6: n = (12 - abs(n)) * -1
    if (n >0) : kierunek = 'lewy'
    else: kierunek = 'prawy'
    n = abs(n)
    if (n == 2):  rodzaj = 'sekstyl'
    elif (n== 3 ): rodzaj = 'kwadratura'
    elif (n== 4 ): rodzaj = 'trygon'
    elif (n== 6 ): rodzaj = 'opozycja'
    else: rodzaj = 'inny'
    if rodzaj != 'inny':
#      print ('Aspekt quesited z sygnifikatorem (%d) kwerenta %s %s %d' % (i, kierunek, rodzaj, n))
#      houses[i].change_colour(colour_way_points)
      aspekty.add(i)
      add_aspekty(i,quesited,rodzaj,kierunek) 
      wynik.append ( (i, quesited) )
  for i in signif_qs:
    n = i - 1     # 1 to kwerent
    if abs(n) > 6: n = (12 - abs(n)) * -1
    if (n >0) : kierunek = 'lewy'
    else: kierunek = 'prawy'
    n = abs(n)
    if (n == 2):  rodzaj = 'sekstyl'
    elif (n== 3 ): rodzaj = 'kwadratura'
    elif (n== 4 ): rodzaj = 'trygon'
    elif (n== 6 ): rodzaj = 'opozycja'
    else: rodzaj = 'inny'
    if rodzaj != 'inny':
#      print ('Aspekt kwerenta z sygnifikatorem (%d) quesited %s %s %d' % (i, kierunek, rodzaj, n))
#      houses[i].change_colour(colour_way_points)
      aspekty.add(i)
      add_aspekty(i,1,rodzaj,kierunek) 
      wynik.append ( (i, 1) )
  # jeżeli wartość bezwzględna > 7:
  # to zmiana znaku i odejmujemy tę wartość od 12
  # wychodzi wartość dodatnia lub ujemna, wtedy aspekt jest lewy/prawy/lewy
  return wynik
  
def company_houses():
  global lista_comp_planets
  pairs = ( (1,2), (3,4), (5,6), (7,8), (9,10), (11,12) )
  wynik = []
  draw_comp_planets_clear()
  lista_planets = []
  d = {} # companies
  for i, j in pairs:
    d['Taka sama figura']  = comp_simple(i,j)   # the same figure
    d['Taka sama planeta'] = comp_demi(i,j)     # demi-simple, the same planet rules
    d['Figury przeciwne']  = comp_compound(i,j) # opposite figures
    d['Taka sama linia głowy'] = comp_capitular(i,j) # head: first Fire line
    r = 0
    if d['Taka sama planeta']: 
      planeta, (n1, n2) = d['Taka sama planeta']
      if d['Figury przeciwne']:  # tylko zwraca 1/0
        planeta += '\nodwrotność'
      lista_planets.append ( ( planeta, (n1, n2) ) ) # planeta, 1, 2
    elif d['Figury przeciwne']:
      lista_planets.append ( ( 'odwrotność', (i, j) )  ) # planeta, 1, 2
      
    for n in d.keys():
      if d[n]: r += 1
    if r:
      wynik.append( (i,j) )
#  if r: print('Pary domów:', wynik)
  for dd in lista_comp_planets:
    print ('==', dd)
  for planeta, (dom1, dom2) in lista_planets:
    draw_comp_planets(planeta, dom1, dom2)
  return wynik

def comp_simple (n1, n2):
  if houses[n1].id == houses[n2].id: return 1
  return 0

def comp_demi (n1, n2):
  if houses[n1].id == houses[n2].id: return 0
  for planeta in houses[n1].planet:
    if planeta in houses[n2].planet: 
#      if len(houses[n2].planet) >1:
#        print ('Planeta wspólna dla domu %s %s: %s' % (n1, n2, planeta))
        return ( planeta, (n1,n2) )
  return 0

def comp_compound (n1, n2):
  if houses[n1].id == houses[n2].id: return 0
  for i in list_compound: # ------------  pary figur przeciwnych
    if houses[n1].name in i and houses[n2].name in i:
      return 1
  return 0

def comp_capitular (n1, n2):
  if houses[n1].id == houses[n2].id: return 0
  if houses[n1].txt[-1] == houses[n2].txt[-1]: return 1
  return 0

def point_index(fortune=0): 
  # liczy albo ukryty czynnik (indeks) albo punkt szczęścia (źródło zasobów)
  # suma pojedynczych kropek w pierwszych 12 polach = domach ==> /12 wskazuje nr domu
  x = 0            # wskazuje ukryty czynnik w sytuacji
  # fortune = punkt szczęścia, źródło wsparcia -- dodajemy wszystkie kropki tych 12 pól
 
  for i in houses.keys():
    for n in houses[i].txt:
      if int (n) == 1 or fortune: x += int (n)
  r = x % 12
  if r == 0: r = 12
#  print (r)
#  print ('Wynik: %d, pełna suma: %d' % (r, x) )
#  houses[r].change_colour(colour_way_points)
  zmiana = ''
  if fortune == 0: 
    btIndex.configure(text = r)
    if houses[r].get_ramka_colour(1) == '': zmiana = 'index'
  else: 
    btFortune.configure(text = r)
    if houses[r].get_ramka_colour(2) == '': zmiana = 'fortune'

  for i in houses: houses[i].clear_colour()
  draw_aspects_clear()
  draw_comp_planets_clear()
  houses[1].change_colour('gray')
  houses[quesited].change_colour('gray')
  if zmiana == 'index':   houses[r].ramka_show(1,'#9b111e')
  elif zmiana == 'fortune': houses[r].ramka_show(2,'#8bb9dd')
  
def fire_the_same(n1, n2):
  s1 = shields[n1].get_text()
  s2 = shields[n2].get_text()
  return s1[-1] == s2[-1]

def add_if_the_same_point (w, list):
  r = []
  for i in list:
    if fire_the_same(w, i): r.append(i)
  return r
  
def way_of_points():
  way = []
  way.insert(0,15) # -------------------------- wstawiam sędziego
  way_neph = []
  way_root = [] # korzeń sytuacji, najwyższa figura
  # ------------------------------------- wstawiam świadków
  way += add_if_the_same_point(15, (13, 14))
  if way: # ------------------------------------- wstawiam kuzynów
    for i in way:
      if i == 13: way_neph += add_if_the_same_point(i, (9,10))
      if i == 14: way_neph += add_if_the_same_point(i, (11,12))
  if way_neph: 
    way_root = way_neph[:]
    way += way_neph
    for i in way_neph: # ------------------------- wstawiam matki i córki
      if i ==  9: way += add_if_the_same_point(i, (1,2))
      if i == 10: way += add_if_the_same_point(i, (3,4))
      if i == 11: way += add_if_the_same_point(i, (5,6))
      if i == 12: way += add_if_the_same_point(i, (7,8))
  if way:
    for i in way:
      shields[i].change_colour(colour_way_points)
  return way

houses = {}
mothers = {}
witness_judge = {}
modes_perfection = {}

root = Tk()
var_canvas_left  = StringVar()
var_canvas_right = StringVar()

canv_houses = ''
canv_shield = ''
canv_mothers = ''
canv_analysis = ''
quesited = 4 # tylko przykładowo, na początek!

root.title('Geomancja')
# --------------------------------------------------- początek lewej części
frame_left = Frame(root); frame_left.pack(side=LEFT,fill=BOTH,expand=1)
frame = Frame(frame_left); frame.pack(fill=X)
# --------------------------------------------------- przyciski paneli
for text, value in [('Tarcza', 'shield'), ('Domy', 'houses'),]:
  Radiobutton(frame, text=text, font = '34', width = 8, value=value, variable=var_canvas_left,
    indicatoron=0,command = lambda: canvas_choose(),
    ).pack(side=LEFT, fill=Y,)
var_canvas_left.set('shield')
Button(frame,text='Koniec',font = '34', width = 8, 
       command = lambda: exit()).pack(side='left')

# --------------------------------------------------- wprowadzenie lewych paneli
frame = Frame(frame_left); frame.pack(fill=BOTH,expand=1)

x = 100; y = 200; h = 230; hp = h/2; h2 = 2 * h
# y -= h/2

canv_shield= Canvas(frame, width = 3 * h,  # background='yellow'
   ); canv_shield.pack(side=LEFT,fill=Y,expand=1,anchor = 'w')

canv_houses = Canvas(frame, width = 3 * h, # background='red'
   ); # canv_houses.pack(side=LEFT,fill=Y,expand=1,anchor = 'w')

  
# --------------------------------------------------- shield
nr = 1
[m1, m2] = (x, y-h/2)
# [m1, m2] = (x, y)
hpx = hp * 0.6
w = h - h/6
shields = {}
for i in range(7,-1,-1): # 0.. 7
  shields[nr] = Shield(nr,canv_shield, m1+(i*hpx),m2,m1+hpx+(i*hpx),m2+w)
  nr += 1

m2 += w
# for i in range(0,8,2): # 6 4 2 0
for i in range(6,-1,-2):
  shields[nr] = Shield(nr,canv_shield, m1+(i*hpx),m2,m1+hpx+(i*hpx),m2+w, 'double')
  nr += 1
  
odstep = h *2
xy = m1, m2+w-odstep, m1+hpx+(7*hpx), m2+w+odstep # m1, m2, m1+hpx+(6*hpx),m1+hpx+8*hpx

odstep = h; xy = m1, m2+w-odstep, m1+hpx+(7*hpx), m2+w+odstep
shields[nr] = Shield(nr,canv_shield, *xy, 'arch', 300, 60, 'right'); nr += 1
shields[nr] = Shield(nr,canv_shield, *xy, 'arch', 180, 60, 'left'); nr += 1
m2 += 15; 
odstep = h; xy = m1, m2+w-odstep, m1+hpx+(7*hpx), m2+w+odstep
shields[nr] = Shield(nr,canv_shield, *xy, 'arch', 240, 60, 'judge')

# canvas_choose()
# --------------------------------------------------- houses
nr = 1; 

for params in ( [x + hp, y + hp, 'r'], [x, y + h, 'l'],
           [x, y + h2, 'd'],           [x + hp, y + h + hp, 'u'],
           [x + h, y + h2, 'd'],       [x + h2, y + h, 'r'],
           [x + h + hp, y + hp, 'l'],  [x + h2, y, 'r'],
           [x + h, y, 'u'],            [x + hp, y + hp, 'd'],
           [x, y, 'u'],                [x, y, 'l'],
           
           ):
  houses[nr] = House(canv_houses, *params[:-1], h, params[-1], nr )
  nr += 1

witness_judge['r'] = House(canv_houses, x + hp+hp/2, y+h,    h, 'd', 'WR')
witness_judge['l'] = House(canv_houses, x + hp/2,    y+h,    h, 'd', 'WL')
witness_judge['j'] = House(canv_houses, x + hp,      y+h+hp *2/3, h, 'd', 'J')


m = 3
# print (canv.itemconfigure(houses[m].id,'fill'))
canv_houses.itemconfigure(houses[m].tr,fill='red'); canv_houses.update()
canv_houses.itemconfigure(houses[m].tr,fill=''); canv_houses.update()

# --------------------------------------------------- początek prawej części
frame_right = Frame(root); frame_right.pack(side=RIGHT,fill=BOTH,expand=1)
frame = Frame(frame_right); frame.pack(fill=X)

# --------------------------------------------------- przyciski paneli
for text, value in [('Dane', 'mothers'), ('Analiza', 'analysis'), ('Testy', 'tests')]:
  Radiobutton(frame, text=text, font = '34', width = 8, 
    value=value, variable=var_canvas_right,
    indicatoron=0,command = lambda: canvas_choose('right'),
    ).pack(side=LEFT, fill=Y)
var_canvas_right.set('mothers')

Button(frame,text='Koniec',font = '34', width = 8, 
       command = lambda: exit()).pack(side='left')

nr = 1
# --------------------------------------------------- wprowadzenie prawych paneli
frame = Frame(frame_right); frame.pack(expand=1,fill=BOTH)

canv_mothers= Canvas(frame, background=colour_mother, # width = 6 * h,  
   ); canv_shield.pack(side=RIGHT,fill=BOTH,expand=1,anchor = 'w')

canv_analysis = Canvas(frame, background=colour_analysis, width = 3 * h,  
   ); # canv_houses.pack(side=RIGHT,fill=BOTH,expand=1,anchor = 'w')

canv_tests = Canvas(frame, background=colour_analysis, width = 3 * h,  
   ); # canv_houses.pack(side=RIGHT,fill=BOTH,expand=1,anchor = 'w')

def my_create_listbox (fr, noScroll = 0, width = 12):
  entryb = Text(fr, font = 'Times 18', width=5, height=1); entryb.pack(fill=X)
  listab = Listbox(fr, font = 'Times 14',width=width) #, highlightthickness=10); 
  if noScroll == 0:
    scroll = Scrollbar(fr, command=listab.yview)
    listab.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
  listab.pack(side=LEFT)
  return listab, entryb

# --------------------------------------------------- matki
frame = Frame(canv_mothers, bg=colour_mother); frame.pack(expand=1,fill=X,anchor='n')
house_order = StringVar()
Label(frame,text = 'Układ domów:', width = 14, font = '34', bg=colour_mother).pack(side=LEFT)
for text, value in [('Naturalny', 'natural'), ('Golden Dawn', 'GD'),]:
  Radiobutton(frame, text=text, font = '34', 
    bg=colour_mother,
    selectcolor=colour_mother,
    activebackground=colour_mother,
    width = 8, value=value, variable=house_order,
    indicatoron=0,command = lambda: houses_configure(),
    ).pack(side=LEFT,fill=X,expand=1)
house_order.set('natural')

# --------------------------------------------------- matki
frame = Frame(canv_mothers); frame.pack()

for i in range(4):
  fram = Frame(frame); fram.pack(side=RIGHT,anchor='n')
  Label(fram,text='Matka %d' % (i+1), font = '24', ).pack(anchor='n')
  listab, entryb = my_create_listbox(fram) 
  mothers[nr] = Mothers(listab)
  mothers[nr].chose_entry(entryb)
  mothers[nr].fill_names()
  nr += 1
      
Label(canv_mothers,bg=colour_mother,width=90).pack()
frame = Frame(canv_mothers); frame.pack()
# --------------------------------------------------- wybór domu
Label(frame,text='Dom - zakres pytania', font = '24', ).pack()
lista_domy, entryb = my_create_listbox(frame,1,14 * 5) 
lista_domy.insert(END, *list_houses)
lista_domy.configure(height= 11)
lista_domy.bind("<Double-Button-1>", lambda event: chosen_lista(lista_domy,entryb,1))
lista_domy.bind("<Return>", lambda event: chosen_lista(lista_domy,entryb,1))

frame = Frame(canv_mothers); frame.pack(side=BOTTOM)
# Button(canv_mothers, text='Wypisywanie', font = '34', command = lambda: wypisywanie()).pack(anchor='w')
Button(frame, text='Czyszczenie', font = '34', command = lambda: czyszczenie()).pack(side=LEFT,anchor='w')
Button(frame, text='Losowanie', font = '34', command = lambda: losowanie()).pack(side=LEFT,anchor='w')

# --------------------------------------------------- analiza

Label(canv_analysis,bg=colour_analysis,width=95).pack()
Button(canv_analysis, text='Losowanie', font = '34', width = 16,
  command = lambda: losowanie()).pack(anchor='w')
Button(canv_analysis, text='Droga punktów', font = '34', width = 16,
  command = lambda: way_of_points()).pack(anchor='w')
Frame(canv_analysis, height = 24).pack()
for n, fn in ( ('Obsadzenie', occupation), ('Koniunkcja', conjunction),
               ('Mutacja', mutation),      ('Translacja', translation),
               ('Aspekty', aspects),       ('Pary domów', company_houses) ):
  fram = Frame(canv_analysis); fram.pack(anchor = W)
  p = Button(fram, font = '34', width = 12); p.pack(side = LEFT)
  odp = Label(fram, text = '1', font = '34', width = 4); odp.pack(side = LEFT)
  modes_perfection[n] = Modes_Perfection(p,odp,n,fn)

Frame(canv_analysis, height = 24).pack()
fram = Frame(canv_analysis); fram.pack(anchor = W)
# ------------------------------------------------------- Index (ukryty czynnik)
Button(fram, text='Indeks', font = '34', width = 14,
  command = lambda: point_index ()).pack(anchor='w', side = LEFT)
btIndex = Label(fram, text = '1', font = '34', width = 2); btIndex.pack(side = LEFT)
fram = Frame(canv_analysis); fram.pack(anchor = W)

# ------------------------------------------------------- Part of fortune (źródło wsparcia)
Button(fram, text='Punkt szczęścia', font = '34', width = 14,
  command = lambda: point_index(1)).pack(anchor='w', side = LEFT)
btFortune = Label(fram, text = '1', font = '34', width = 2); btFortune.pack(side = LEFT)


# --------------------------------------------------- testy
var_tests_obsadzenie = BooleanVar()
var_tests_koniunkcja = BooleanVar()
var_tests_mutacja = BooleanVar()
var_tests_translacja = BooleanVar()
var_tests_aspekty = BooleanVar()
var_tests_company_houses = BooleanVar()
var_tests_impedition = BooleanVar()

f = Frame(canv_tests, bg = colour_analysis); f.pack(anchor=W)

for tekst, variable in (
   ('Obsadzenie', var_tests_obsadzenie), ('Koniunkcja', var_tests_koniunkcja),
   ('Mutacja', var_tests_mutacja),      ('Translacja', var_tests_translacja),
   ('Aspekty', var_tests_aspekty),       ('Pary domów', var_tests_company_houses),
   ('Impedition', var_tests_impedition),
   ):
  Checkbutton(f,text=tekst, font = 40, indicatoron=0,
    variable = variable, 
  ).pack(anchor='w')


Label(canv_tests,bg=colour_analysis,width=95).pack()


Button(canv_tests, text='Test', font = '34', 
  command = lambda: testuj()).pack(side=LEFT,anchor='w')

Button(canv_tests, text='Test funkcji', font = '34', 
  command = lambda: test_funkcji()).pack(side=LEFT,anchor='w')


  
p = Button(canv_tests, font = '34'); p.pack(side=LEFT,anchor='w')
# button, opis, function
odpp = Label()
modes_perfection['Occupation F'] = Modes_Perfection(p,odpp,'Obsadzenie F',occupation)

Button(canv_tests, text='Tło tarczy', font = '34', 
  command = lambda: shields[13].change_colour('red')).pack(side=LEFT,anchor='w')

# for i in range(15):  print (i+1, shields[i+1].nr)

canvas_choose('right')
losowanie()
root.state('zoomed')
# houses[1].ramka_show('red')
mainloop()
