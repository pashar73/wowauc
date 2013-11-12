#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import sys
import wowapi

OPERATION_ADD = 0
OPERATION_DEL = 1
OPERATION_PRINT = 2

Operation = OPERATION_PRINT
ItemID = 0
Price = 0

ItemNames = {}

def Usage():
  print "Usage:"
  print "watch.py --add <ID> <price>"
  print "watch.py --del <ID>"
  print "watch.py --print"

def ProcessOptions():
  global Operation
  global ItemID
  global Price
  try:
    if sys.argv[1] == "--add":
      Operation = OPERATION_ADD
      ItemID = int(sys.argv[2])
      Price = int(sys.argv[3])
    elif sys.argv[1] == "--del":
      Operation = OPERATION_DEL
      ItemID = int(sys.argv[2])
    elif sys.argv[1] == "--print":
      Operation = OPERATION_PRINT
  except IndexError:
    Operation = OPERATION_PRINT
    Usage()

def GetWatchList(fname):
  listfile = open(fname)
  wlist = eval(listfile.read())
  listfile.close()
  return wlist

def __Print__(lst):
  for rec in lst:
    print rec["name"], ":", rec["price"],"(", rec["id"],")"

if __name__ == "__main__":
  Modified = False
  WatchList = GetWatchList("watchlist.txt")

  #ItemNames = wowapi.LoadItemNames("itemdata.txt")
  ItemNames = wowapi.ItemNames("itemdata.txt")

  ProcessOptions()

  if Operation == OPERATION_ADD:
    ItemToUpdate = next((it for it in WatchList if it["id"] == ItemID), None)
    if ItemToUpdate == None:
      WatchList.append({"id": ItemID, "price": Price, "name":""})
    else:
      ItemToUpdate["price"] = Price
    Modified = True
  elif Operation == OPERATION_DEL:
    for item in WatchList:
      if item["id"] == ItemID:
        WatchList.remove(item)
        Modified = True
        break
  elif Operation == OPERATION_PRINT:
    __Print__(WatchList)

  # Update names
  for item in WatchList:
    if item["name"] == "":
      item["name"] = ItemNames.GetName(item["id"])

  if Modified:
    listfile = open("watchlist.txt", "w")
    listfile.write(repr(WatchList))
    listfile.close()

