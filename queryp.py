#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import sys
import wowapi
import json
import bz2

factions = ["alliance", "horde", "neutral"]

itemID = int(sys.argv[1])

with bz2.BZ2File("aucdata.txt.bz2","r") as jfile:
  JSdata = json.load(jfile)

Names = wowapi.ItemNames("itemdata.txt")
itemName = Names.GetName(itemID)

AllItems = JSdata[wowapi.Faction]["auctions"]
items = [x for x in AllItems if x["item"] == itemID]

items.sort(key=lambda z: z["buyout"]/z["quantity"])

print "Prices for", itemName
for x in items:
    print "bid: ", x["bid"], "buyout:", x["buyout"], "stack:", x["quantity"], "buyout per unit:", x["buyout"]/x["quantity"], "owner:", x["owner"].encode('utf-8')
