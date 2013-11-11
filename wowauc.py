#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import sys
import wowapi
import json
import watch
import bz2

optPrintNames = True
optForceUpdate = False
optForcePrint = False
optDontLoad = False


ItemNames = {}

def ProcessOptions():
  global optPrintNames
  global optForceUpdate
  global optForcePrint
  global optDontLoad
  for opt in sys.argv:
    if opt == "--nonames":
      optPrintNames = False
    elif opt == "--force":
      optForceUpdate = True
    elif opt == "--print":
      optForcePrint = True
    elif opt == "--noload":
      optDontLoad = True


  
def OwnerString(x):
  if optPrintNames:
    return "owner: " + x["owner"].encode('utf-8')
  else:
    return " "

ItemsToWatch = watch.GetWatchList("watchlist.txt")

ProcessOptions()

try:
  urldata = wowapi.FetchUpdateFileAndURL()
except Exception as excp:
  exit(1)

if wowapi.CheckIsUpdated(urldata, "lastupdate.txt") | optForceUpdate:
  if not optDontLoad:
    wowapi.FetchFullAucData(urldata)
elif not optForcePrint:
  exit()

#ItemNames = wowapi.LoadItemNames("itemdata.txt")
ItemName = wowapi.ItemNames("itemdata.txt")

fdata = bz2.BZ2File("aucdata.txt.bz2", "r")
JsonAucData=json.load(fdata)
fdata.close()
AllItems = JsonAucData[wowapi.Faction]["auctions"]
for item in ItemsToWatch:
  items = [x for x in AllItems if (x["item"] == item["id"]) & (x["buyout"] != 0) & (x["buyout"]/x["quantity"]  <= item["price"]) ]
  #if item["id"] not in ItemNames.keys():
  #  wowapi.UpdateItemNames(item["id"], "itemdata.txt", ItemNames)
  iname = ItemName.GetName(item["id"])

  print "   ", iname
  items.sort(key=lambda z: z["buyout"]/z["quantity"])

  for x in items:
    print "bid: ", x["bid"], "buyout:", x["buyout"], "stack:", x["quantity"], "buyout per unit:", x["buyout"]/x["quantity"], OwnerString(x)



