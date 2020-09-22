#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests as req
import sys

# InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##########################################
# Переменные
if (len(sys.argv) == 1):
  print ("Добавте номер телефона! например ", sys.argv[0], '9025111111"')
  sys.exit()
elif len(sys.argv) == 2:
  if (sys.argv[1]):  tnum = sys.argv[1]

url = "https://zniis.ru/bdpn/check/?num="

phones = []

##########################################
# Функция поиска номера в базе принимает на вход url и номер телефона
def search_base(url,tnum):
  url += tnum
  resp = req.get(url, verify=False)
  soup = BeautifulSoup(resp.text, 'lxml')
  # Пока есть такой стиль в div с данными, привязываемся к нему
  # <div class="column_attr clearfix" style="background-color:#f8f9fd;padding:30px;"><b>9025111111</b> "Т2 Мобайл" ООО<br/>
  x = soup.body.find('div' , attrs={'class' : 'column_attr clearfix', 'style': 'background-color:#f8f9fd;padding:30px;'})
  x = x.text
  x = "\n".join([ll.rstrip() for ll in x.splitlines() if ll.strip()])  # много пустых строк - убираем их
  #x = x.replace('\n\n','\n').replace('\n\n','\n')  # много пустых строк - убираем их
  return x

##############################
# Алгоитм поиска номера с запросом в функции search_base
# параметр поиска - номер телефона(tnum)
# 9025111111 - str, tnum.isnumeric()
# 9025111111,9025222222,9086333333 - str, tnum.split(',')[0].isnumeric()
# phones.txt - str, NOT tnum.split(',')[0].isnumeric()
if tnum.isnumeric() == 1:
  n= tnum
  x = search_base(url,n)
  print (x)
else:
  if tnum.split(',')[0].isnumeric() == 1:
    for n in tnum.split(','):
      x = search_base(url,n)
      print (x)
      phones.append(x)
  else:
    phones_txt = sys.argv[1]
    f = open(phones_txt, 'r')
    phones = [line.strip() for line in f]
    tnum = phones[0]
    for n in tnum.split(','):
      x = search_base(url,n)
      print (x)
      phones.append(x)
    f.close()

##################################
# Записываем данные в файл построчно из списка phones[]
f = open('providers.txt', 'w')
f.writelines( "%s\n" % item for item in phones )
f.close()

