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
  
  main = DiscordLevelUp("ODk4MTk2ODQ2NzkzNjEzMzUz.YeSD-Q.KNiOUUUSx4MwMk1h34syctrEdKs", messages, worker_file)

  main.add_server("929436445159096391", 303)
  main.add_server("929436444475392047", 62)
  main.sendMessages()


time.sleep(1000000)
