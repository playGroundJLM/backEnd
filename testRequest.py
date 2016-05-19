# import requests
# url = 'https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034|36.455556,-116.866667&key=AIzaSyDSm_uEB6ImW4x5Az6ghGocQ977id4LYzs'
# res = requests.get(url)
# print(res.json())
#

from osmapi import OsmApi

api = OsmApi()
map = api.Map(31.766597, 35.174405, 31.786225, 35.212256)
api.ParseOsm("./Jerusalem.osm.pbf")
print(map)
