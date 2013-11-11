# -*- coding: utf-8 -*

import json
import urllib2
import urllib
import bz2

WoWrealm = u"Борейская тундра"
WoWhost = u"eu.battle.net"
WoWauctionUrl = u"/api/wow/auction/data/"
Faction = "alliance"
WoWitemUrl = u"/api/wow/item/"

def LoadItemNames(fname):
  dataf = open(fname)
  items = {}
  for line in dataf:
    if len(line.strip()) == 0:
      continue
    item = json.loads(line)
    items[item["id"]] = item["name"]
  dataf.close()
  return items

def UpdateItemNames(ItemId, fname, ItemNames):
  print "Updating item ", ItemId
  dataf = open(fname,"a")
  jsonURL = u"http://" + WoWhost + WoWitemUrl + str(ItemId)
  url = urllib2.urlopen(jsonURL)
  itemstr = url.read()
  dataf.write('\n')
  dataf.write(itemstr)
  dataf.close()
  ItemObj = json.loads(itemstr)
  ItemNames[ItemObj["id"]] = ItemObj["name"]

class ItemNames:
  def __init__(self, fname):
    self.filename = fname
    self.items = {}
    with open(self.filename, "r") as dataf:
      for line in dataf:
        if len(line.strip()) == 0:
          continue
        item = json.loads(line)
        self.items[item["id"]] = item["name"]

  def update_names(self, ItemID):
     print "Updating item ", ItemID
     dataf = open(self.filename,"a")
     jsonURL = u"http://" + WoWhost + WoWitemUrl + str(ItemID)
     url = urllib2.urlopen(jsonURL)
     itemstr = url.read()
     dataf.write('\n')
     dataf.write(itemstr)
     dataf.close()
     ItemObj = json.loads(itemstr)
     self.items[ItemObj["id"]] = ItemObj["name"]
  
  def GetName(self, ItemID):
    if not (ItemID in self.items.keys()):
      self.update_names(ItemID)
    return self.items[ItemID]

def CheckIsUpdated(data, fname):
  try:
    dataf = open(fname)
    js = json.load(dataf)
    last_update = js["files"][0]["lastModified"]
    dataf.close()
  except IOError:
    last_update = 0

  dataf = open(fname,"w")
  dataf.write(data)
  dataf.close()
  js = json.loads(data)

  return last_update != js["files"][0]["lastModified"]

def FetchUpdateFileAndURL():
  jsonURL = u"https://" + WoWhost + WoWauctionUrl + urllib.quote(WoWrealm.encode('utf8'))
  url = urllib2.urlopen(jsonURL)
  return url.read()

def FetchFullAucData(urldata):
  print "Loading new data"
  AucObj = json.loads(urldata)
  AucQueryURL = AucObj[u"files"][0][u"url"]

  AucData=urllib2.urlopen(AucQueryURL)

  fdata = bz2.BZ2File("aucdata.txt.bz2", "w")
  fdata.write(AucData.read())
  fdata.close()

