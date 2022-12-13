import json
import sqlite3

# SQLite Database name
DB_Name =  "mqtt.db"

# Database Manager Class

class DatabaseManager():
        def __init__(self):
                self.conn = sqlite3.connect(DB_Name)
                self.conn.execute('pragma foreign_keys = on')
                self.conn.commit()
                self.cur = self.conn.cursor()

        def add_del_update_db_record(self, sql_query, args=()):
                self.cur.execute(sql_query, args)
                self.conn.commit()
                return

        def __del__(self):
                self.cur.close()
                self.conn.close()

# Functions to push Data into Database

# Function to save NMAP VALUES to DB Table
# If no vendor available then only insert 2x values(ip and mac)
def Nmap_Data_Handler(jsonData):
    json_Dict = json.loads(jsonData)
    try:
     for x in json_Dict:
      if 'vendor' in x:
          ipv4 = x['ipv4']
          mac = x['mac']
          vendor = x['vendor']
      else:
          ipv4 = x['ipv4']
          mac = x['mac']

      #Push into DB Table
      dbObj = DatabaseManager()
      dbObj.add_del_update_db_record("INSERT OR IGNORE INTO data (ipv4, mac, vendor) values (?,?,?)",[ipv4, mac, vendor])
      del dbObj
     print("")
     print("Data has been inserted into Database.")
     print("")
    except Exception as e:
        print(e)

# Master Function to Select DB Funtion based on MQTT Topic

def sensorDataHandler(Topic, jsonData):
        if Topic == "mqtt/csibman27":
                Nmap_Data_Handler(jsonData)
        #elif Topic == "mqtt/csibman27/otherdata":
                #otherdata(jsonData)
