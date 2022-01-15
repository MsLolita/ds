import requests
import random
import time
from datetime import datetime
import json
import threading
import pathlib, os

class DiscordLevelUp:
  def __init__(self, authorization, messages, worker_file):
    self.headers = {
      'authority': 'discord.com',
      'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
      'x-debug-options': 'bugReporterEnabled',
      'accept-language': 'uk',
      'sec-ch-ua-mobile': '?0',
      'authorization': authorization,
      'content-type': 'application/json',
      'sec-ch-ua-platform': '"Windows"',
      'accept': '*/*',
      'origin': 'https://discord.com',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty'
    }
    self.messages = messages
    self.worker_file = worker_file

    self.server_ids = []
    self.min_delays = []

  def sendMessage(self, server_id, message):
    data = json.dumps({"content": message})

    response = requests.post('https://discord.com/api/v9/channels/' + str(server_id) + '/messages', headers=self.headers, data=data, proxies={"https" : "http://oHXOMY:uIJ0LLa6Ai@46.8.23.244:5500"})
    return response
  
  def sendMessages(self):
    for i in range(len(self.server_ids)):
      main_thread = threading.Thread(target=lambda: self.sending(self.server_ids[i], self.min_delays[i]))
      main_thread.start()
      time.sleep(random.uniform(2, 5))

  def sending(self, server_id, min_delay):
    for message in self.messages:
      res = self.sendMessage(server_id, message)
      msg_id = str  
      try:  
        msg_id = res.json()["id"]
      except: 
          print(res.text)  
          time.sleep(20)
          continue
      log(msg_id, message)

      del_first_line_file(self.worker_file)
      if server_id != self.server_ids[0]:
        self.del_msg(server_id, msg_id)    
        #  if server_id == "929363885872521306":  
        #    del_first_line_file(self.worker_file)
        #  else: self.del_msg(server_id, msg_id)
          # print(message, res.text)
          
      time.sleep(random.uniform(min_delay + 1, min_delay + 2))

  def del_msg(self, server_id, msg_id):
    requests.delete(f'https://discord.com/api/v9/channels/{server_id}/messages/{msg_id}', headers=self.headers)
      
  def add_server(self, server_id, min_delay):
    self.server_ids.append(server_id)
    self.min_delays.append(int(min_delay))

def log(msg_id, msg, file="logs.txt"):
  log = datetime.now().strftime("%H:%M:%S") + " | " + str(msg_id) + " | " + msg
  print(log)
  with open(file, 'a', encoding='utf-8') as f:
    f.write(log + "\n")

def make_list_from_file(file):
  with open(file, 'r', encoding='utf-8') as f:
    return [x for x in f.read().split("\n") if x]

def shuffle_file(file):
    lines = open(file).readlines()
    random.shuffle(lines)
    open(file, 'w').writelines(lines)

def create_worker_file(worker_file, main_file="messages.txt"):
    with open(main_file,'r', encoding='utf-8') as main_file, open(worker_file,'a', encoding='utf-8') as worker_file:
          
        # read content from first file
        for line in main_file:
                   
             # append content to second file
             worker_file.write(line)

def del_first_line_file(file):
    # прочитаем файл построчно
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # запишем файл построчно пропустив первую строку
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(lines[1:])

if __name__ == '__main__':
  worker_file = "worker.txt"
  main_file = "msgs.txt"
  
  messages = make_list_from_file(worker_file)
  
  main = DiscordLevelUp("NDk1MzA0ODYzNTc2NzUyMTM0.YeH8QA.JOqFvloovs_JZcTS6mCAwkwFNVE", messages, worker_file)

  main.add_server("930102591923294228", 122)
  main.add_server("931600696594284654", 122)
  #main.add_server("929427655462379620", 62)
  #main.add_server("928072746083188847", 54)  # chine 928072746083188847
  # main.add_server("928072819881955359", 34)  # japan 928072819881955359
  # main.add_server("928072857580347493", 34)  # korean 928072857580347493
  # main.add_server("929096939230879824", 34)  # hindi 929096939230879824
  # main.add_server("928516544621867058", 34)  # dutch 928516544621867058
  # main.add_server("929109408351395920", 34)  # french 929109408351395920
  # main.add_server("928072904497852446", 34)  # spanish 928072904497852446
 # main.add_server("928073050107314196", 34)  # italian 928073050107314196
  # main.add_server("928073004322283550", 34)  # german 928073004322283550
  # main.add_server("928072781973831701", 34)  # indonesian 928072781973831701
  # main.add_server("928516201917841409", 34)  # philliphine 928516201917841409
    
    
  # main.add_server("926068232354414633", 35) 
  main.sendMessages()

  

  # berok = DiscordLevelUp("ODk1MTY2Nzc0ODM4OTYwMTY4.YWrvQg.FW8wRvymfoAE1ugAPQwMtC3uMrE", messages, worker_file)

  # berok.add_server("929363885872521306", 63)
  #berok.add_server("929363885671215152", 42)# turkich 929363885671215152
  #berok.add_server("929384159552626759", 42)# dutch 929384159552626759
  #berok.add_server("929363885469876237", 62)# general 929363885469876237
  #berok.add_server("929391884919525377", 28)# indian 929391884919525377
    
    
    
  # berok.sendMessages()
  # lechko = DiscordLevelUp("ODkwMjM3NDc5ODkyOTYzMzI4.YVyGOA.VdJvfTC6N5s0rjUZ_2KV6z4nhMk")
  # lechko.add_server("885436021125312532", 13)
  # lechko_thread = threading.Thread(target=lechko.sendMessages)
  # lechko_thread.start()
# oblik NDk1MzA0ODYzNTc2NzUyMTM0.YViPTg.jWHVmxkeNMe8sz9fPo6lrghsdPU
# mofarok 1profile adspower ODk4MTkzMzk0OTE0OTgzOTY3.YWgp9g.SFe6G70c-Z6zjv_mWVAG1xEqTds
# profile_3_cofob ODk4MTk3NjEyNTUxODY4NDE2.YWgt5g.73pIJVwYpQ_fGW13gy7ZxxY_ChU


time.sleep(100000)
