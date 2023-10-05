import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../creds/gs_creds.json"
os.environ["PATH_2_GS_INDEX"] = "gs://data-nodes-index/index.csv" 
os.environ["OK-status"] = 200
os.environ["ERROR-status"] = 400
