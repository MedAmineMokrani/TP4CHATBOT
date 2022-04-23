import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import random
from datetime import datetime
from pytz import timezone
import requests


hostname="127.0.0.1:8000"
apikey="FAIEenSQsbvsj4VmJM4qcq4NW4dyVaX1"



logging.basicConfig(filename='bot.log', filemode='w' ,level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',)


load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True  
bot = commands.Bot(command_prefix="!", intents=default_intents)

class MyBot(commands.Bot): 
    
    def __init__(self):
        super().__init__()
        
    @bot.event
    async def on_ready():
        print("le Bot a réussi à se connecter.")
        logging.info('le Bot a réussi à se connecter.')
    


    @bot.event
    async def on_member_join(member):
        print(f"L'utilisateur {member.display_name} a rejoint le serveur !")
        channel = bot.get_channel(959350653979869217)
        await channel.send(f"Bonjour {member.display_name} vu que vous êtes un nouveau membre dans notre serveur vous pouvez taper '!help' pour voir les commandes disponibles")
        logging.info(f"L'utilisateur {member.display_name} a rejoint le serveur !")
           

    @bot.event
    async def on_message(message):
        try:
            if message.content.startswith("!del"):
                number = int(message.content.split()[1])
                messages = await message.channel.history(limit=number + 1).flatten()
                for each_message in messages:
                    await each_message.delete()
                logging.info(f"le membre {message.author} a supprimer des messages")
            
        except Exception as e:
            logging.info(f"une erreur %s ",e)
            
        if message.content.lower() == "!help":
                await message.channel.send("Voila les commandes disponible dans ce serveur : \n\n 1 - !del x : Vous donne la possibilité de supprimer les x derniers messages. Exemple d'utilisation !del 5\n\n 2 - !random x y : Vous donne la possibilité de générer un chiffre aléatoire entre x et y. Exemple d'utilisation !random 5 10\n\n3 - !localisation ip  x : Vous donne la possibilité de voir la localisation exacte de l'ip donné en paramétre et l'afficher sur une carte. Exemple d'utilisation !localisation ip  8.8.8.8\n\n")
                logging.info(f"le membre {message.author} a utiliser la commande !help.")
        try:         
            if message.content.startswith("!random"):
                firstnumber = int(message.content.split()[1])
                secondnumber = int(message.content.split()[2])
                x = random.randrange(firstnumber, secondnumber)
                await message.channel.send(x)
                logging.info(f"le membre {message.author} a génerer un nombre entre %s et %s",firstnumber , secondnumber)
        except Exception as e:
            logging.info(f"une erreur %s ",e)
    
        
                            
        try:       
            
            if message.content.startswith("!localisation ip"):
           
                ip = (message.content.split()[2])
                url = "http://%s" % (hostname) + "/ip/%s" % ip + "?key=%s" % apikey
                r = requests.get(url).json()
                lat = r["Latitude"]
                lon = r["Longitude"]
             
                openstreetmap = "https://www.openstreetmap.org/?mlat=%s" % (lat) + "&mlon=%s" % lon
        
                
                await message.channel.send(openstreetmap)
                logging.info(f"le membre {message.author} a utiliser la commande !localisation pour cette IP : %s ",ip)
        except Exception as e:
            logging.warn(f"une erreur %s ",e)




bot.run(os.getenv("TOKEN"))