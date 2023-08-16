import re
import pandas as pd
import openai
import time
import numpy as np


features_cleaned = pd.read_csv("test_set.csv", sep= ";",index_col=0)
grouped_features = features_cleaned.groupby(["id_of_the_features"])["name_of_the_features"].unique()
keys= features_cleaned.id_of_the_features.unique()


class ChatGPT:
    def __init__(self, api_key, rolle):
        openai.api_key = api_key
        self.dialog = [{"role":"system","content":rolle}]
        
        
    def fragen(self,frage):

        self.dialog.append({"role":"user","content":frage})
        ergebnis =  openai.ChatCompletion.create( model = "gpt-3.5-turbo", messages = self.dialog )
        antwort = ergebnis.choices[0].message.content
        self.dialog.append({"role":"assistant","content":antwort})
        return antwort


 
length_chat_gpt = len(features_cleaned) 
    
check_points = [0,100,  50, 150, 200, 125, 250, 300, 350, 400, 2250 ]
        
for x  in range(202,length_chat_gpt):
    try:
        with open("api.key", "r") as api_key:
            API_KEY = api_key.read()
        chat_gpt = ChatGPT(API_KEY, "Sei ein Data Scientist!")
        liste=grouped_features[features_cleaned["id_of_the_features"][x]]
        mylist=",".join(map(str,liste))
        frage= "Try to set a range of values for the feature:" +features_cleaned["name_of_the_features"][x]+ "that comes from a dataset. Keep the answer as short as possible, just show the min and the max." +"Here is the Datasetdescription: "+ features_cleaned.data_descr[x].replace("\n", "") +". And here is a list of all Features of this Dataset:" + mylist
        antwort = chat_gpt.fragen(frage)
        features_cleaned["chat_gpt_desc_feature"][x] = antwort
        print(x)
        
        if x in check_points:
            features_cleaned.to_csv("Test_erweitert.csv",sep = ";")
            print("saved")
        time.sleep(20)
    except:
        print("fehler")


    
features_cleaned.to_csv("Test_3_2_erweitert.csv",sep = ";")
features_cleaned.to_csv("Test_3_erweitert.csv",sep = ";")




