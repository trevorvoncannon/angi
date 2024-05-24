import requests
from pathlib import Path
import time
import sys

api_url = "https://gutendex.com/books" # API url you are querying
directory = "./api-data/" # Parent directory you want the data to be place in

def api_request(api_url):
   try:
     r = requests.get(api_url)
     r.raise_for_status()
   except requests.exceptions.Timeout as et:
      print ("Timeout:", et)
      sys.exit(1)
   except requests.exceptions.ConnectionError as ec:
      print ("Connection Error:", ec)
      sys.exit(1)
   except requests.exceptions.HTTPError as eh:
      print ("HTTP Error:", eh)
      sys.exit(1)
      
   data = r.text
   return data

def write_data(data, directory):
  timestamp = time.strftime("%Y%m%d-%H%M%S")
  file = Path(directory + "api-data-" + timestamp + ".json")
  file.parent.mkdir(exist_ok=True, parents=True)
  file.write_text(data)
  
if __name__ == "__main__":
   write_data(api_request(api_url), directory)
