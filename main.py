#!/usr/bin/env python
from JetFileII import Message, TextFile , PictureFile, SEQUENTSYS
import time
from socket import *
import requests
import json
import sys
import argparse


verbosity = False


def generateTextScreen(text, name="AA.nmg"):
    return TextFile(text , name , drive="E")

def generateInfoScreen():
  return TextFile('{top}{center}{raindropsin}{red}Dali vali?{nl}{nl}NE', "AB.nmg", drive='E')

def generateVali():
   return TextFile("{top}{center}{amber}NE" , "AA.nmg", drive="E")


def debug_print(str):
    if(verbosity):
        print(str)

def generateBTCScreen():
  r = requests.get('https://api.coinmarketcap.com/v2/ticker/1/')
  r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
  jsonObject = r.json()
  btcprice = int(jsonObject["bpi"]["USD"]["rate_float"])
  percent_change_24h = 0 #float(jsonObject["data"]["quotes"]["USD"]["percent_change_24h"])
  percent_change_7d = 0 #float(jsonObject["data"]["quotes"]["USD"]["percent_change_7d"])
  color24 = '{green}'
  color7d = '{green}'
  if percent_change_24h < 0 :
    color24 = '{red}'
  if percent_change_7d < 0 :
    color7d = '{red}'
  change24 = '{color}{value:+.1f}'.format(color=color24, value=percent_change_24h)
  change7d = '{color}{value:+.1f}'.format(color=color7d, value=percent_change_7d)
  return TextFile('{wipeupwardin}{wipeupwardout}\x14DD{middle}%s{b16x12}{halfspace}$%s{nl}{7x6}{amber}BTC %sd %sw' % ( color24, '{:,d}'.format(btcprice), change24, change7d ), 'AC.nmg', drive='D')

def main(ip="172.16.16.2" , port=9520 , texts=""):

    ser = socket(AF_INET, SOCK_STREAM)
    addr = (ip, port)

    ser.connect(addr)
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
    parser.add_argument("--text" , "-t", help="Show the given text", type=str, required=True, nargs="*")
    parser.add_argument("--verbose","-v" , help="Show debug messages", required=False, default=False)
    args = parser.parse_args()
    verbosity = args.verbose
    texts = args.text
    ip = args.address
    port = args.port
    main(ip=ip, port=port ,texts=texts)