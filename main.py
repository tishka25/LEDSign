#!/usr/bin/env python
from JetFileII import Message, TextFile , PictureFile, SEQUENTSYS, Symbols
import time
from socket import *
import requests
import json
import sys
import argparse
from struct import *
import io


verbosity = False

def replaceAllSymbols(text):
  formated_data = []
  for ch in text.decode("utf8"):
  # for i in range(len(text)):
    # ch = text[i]
    print("Char: " + hex(ord(ch)))
    # if ord(ch) > ord("}"):
      
    formated_data.append(ch)
    
  return "".join(formated_data)



def generateTextScreen(text, name="AA.nmg"):
    return TextFile(text , name , drive="E")

def generateInfoScreen():
  return TextFile('{top}{center}{raindropsin}{red}Dali vali?{nl}{nl}NE', "AB.nmg", drive='E')



def debug_print(str):
    if(verbosity):
        print(str)

def main(ip="172.16.16.2" , port=9520 , texts=""):

    ser = socket(AF_INET, SOCK_STREAM)
    addr = (ip, port)

    ser.connect(addr)

    # Turn Sign On
    ser.send(Message.TurnSignOn())
    time.sleep(0.2)
    #

    files = []
    if True:
        for i in range(len(texts)):
            files.append(generateTextScreen(str(texts[i]) , name=str(i) + ".nmg"))
        for f in files:
            debug_print("Writing file..." + f.label + " to drive: " + f.drive)
            if f.type == 'T':
                data = Message.WriteTextFilewithChecksum(f)
                debug_print(data)
                ser.send(data)
            elif f.type == 'P':
                for packetNumber in range(0,f.numPackets):
                    debug_print("Writing image " + f.label + " do drive: " + f.drive + " packet number: " + str(packetNumber))
                    ser.send(Message.WritePictureFileWithChecksum(f, packetNumber=packetNumber))
            time.sleep(0.2)

        ss = SEQUENTSYS(files)
        # just write the playlist as a system file
        playlist = Message.WriteSystemFile(ss)
        debug_print("Writing playlist...")
        debug_print(playlist)
        ser.send(playlist)
        debug_print("Script complete.")
        ser.close()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    parser.add_argument("--address", "-a", help="The IP address of the connected LED Sign", type=str ,required=True)
    parser.add_argument("--port" , "-p" , help="The Port of the connected LED Sign" , type=int , required=False, default=9520)
    parser.add_argument("--text" , "-t", help="Show the given text", type=str, required=False, nargs="*")
    parser.add_argument("--file" , "-f" , help="Show text from the given file", type=str, required=False)
    parser.add_argument("--verbose","-v" , help="Show debug messages", required=False, default=False)
    args = parser.parse_args()
    verbosity = args.verbose
    texts = []
    if(args.text):
      texts = args.text
    if(args.file):
      file = io.open(args.file, "rU", encoding="utf8") 
      file_content = file.read().encode("utf8")
      # file_content = replaceAllSymbols(file_content)
      # print(file_content)
      texts = [file_content]
    ip = args.address
    port = args.port
    # main(ip=ip, port=port ,texts=[Symbols['?']])
    print(texts)
    main(ip=ip, port=port ,texts=texts)