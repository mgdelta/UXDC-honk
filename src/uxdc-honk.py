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

import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

#sys.path.insert(1, os.path.join(sys.path[0], '../_protobuf'))

import UXDC_Honk_pb2

def main():
  # print eCAL version and date
  print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
  
  # initialize eCAL API
  ecal_core.initialize(sys.argv, "UXDC-HonkApp")
  
  # set process state
  ecal_core.set_process_state(1, 1, "I feel good")

  # create publisher
  pub_status = ProtoPublisher("UXDC_Honk_Status", UXDC_Honk_pb2.HONK_Status)
  
  status = UXDC_Honk_pb2.HONK_Status()
  status.alive_counter = 0
  
  # create person instance and set content
  #person = person_pb2.Person()
  #person.name        = "Max"
  #person.stype       = person_pb2.Person.MALE
  #person.email       = "max@mail.net"
  #person.dog.name    = "Brandy"
  #person.house.rooms = 4
  
  # send messages
  while ecal_core.ok():
  
    status.alive_counter = status.alive_counter + 1
    pub_status.send(status)
    
    # sleep 100 ms
    time.sleep(0.5)
  
  
  
  # finalize eCAL API
  ecal_core.finalize()
  
if __name__ == "__main__":
  main()  
