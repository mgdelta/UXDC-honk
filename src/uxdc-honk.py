# ========================= eCAL LICENSE =================================
#
# Copyright (C) 2016 - 2019 Continental Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ========================= eCAL LICENSE =================================

import os
import sys
import time
import threading

import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

import libioplus as relay_shield

#sys.path.insert(1, os.path.join(sys.path[0], '../_protobuf'))

import UXDC_Honk_pb2

#def callback(topic_name, person, time):
#  print("")
#  print("Received person ..")
#  print("person id    : {}".format(person.id))
#  print("person name  : {}".format(person.name))
#  print("person stype : {}".format(person.stype))
#  print("person email : {}".format(person.email))
#  print("dog.name     : {}".format(person.dog.name))
#  print("house.rooms  : {}".format(person.house.rooms))


def blinker_toggle(statuspackage):
  relay_shield.setRelayCh(0, 1, 1)
  time.sleep(0.4)
  relay_shield.setRelayCh(0, 1, 0)
  statuspackage.hazard_blinker_active = not statuspackage.hazard_blinker_active
  
def secure_relay_init():
  relay_shield.setRelays(0,0)  

def do_send_status(publisher, statuspackage):
  while True:
    statuspackage.alive_counter = statuspackage.alive_counter + 1
    publisher.send(statuspackage)
    time.sleep(0.5)

def switch_honk_mode(mode):
  if (mode == True):
    print('Changing Honk mode to UXDC mode...')
  else:
    print('Changing Honk mode to VW mode...')
    
def honk_child_warning():
  print('Honk: Warning child left behind')



def main():
  # print eCAL version and date
  print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
  
  # make sure all Relays are in off state
  secure_relay_init()
  
  # initialize eCAL API
  ecal_core.initialize(sys.argv, "UXDC-HonkApp")
  
  # set process state
  ecal_core.set_process_state(1, 1, "I feel good")

  # create publisher
  pub_status = ProtoPublisher("UXDC_Honk_Status", UXDC_Honk_pb2.HONK_Status)
  
  status = UXDC_Honk_pb2.HONK_Status()
  status.alive_counter = 0
  status.hazard_blinker_active = False
  status.honk_mode_status = status.UNKNOWN
  
  honk_mode_status = False

  # create subscriber and connect callback
  #sub = ProtoSubscriber("person", person_pb2.Person)
  #sub.set_callback(callback)  
  t = threading.Thread(target=do_send_status, args=[pub_status, status])
  t.start()
  
  # send messages
  while ecal_core.ok():
  

    blinker_toggle(status)
    #print(status.hazard_blinker_active)
    
    
    #pub_status.send(status)
    #do_send_status(pub_status,status)
    
    switch_honk_mode(honk_mode_status)
    honk_mode_status = not honk_mode_status
    
    if honk_mode_status:
      status.honk_mode_status = status.UXDC_MODE
    else:
      status.honk_mode_status = status.VW_MODE


    # sleep 100 ms
    time.sleep(1.0)
  
  
  
  # finalize eCAL API
  ecal_core.finalize()
  
if __name__ == "__main__":
  main()  
