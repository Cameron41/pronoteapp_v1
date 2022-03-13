import discord
import pronotepy
from pronotepy.ent import ac_orleans_tours
from time import sleep
from random import choice
from discord.ext import commands, tasks
import asyncio
from itertools import cycle

# Création d'une instance
client = discord.Client()
TOKEN = 'OTUyMzAyNDE1NzgzMjY4NDEy.Yi0CvA.lf5RpBjU5imIgBiSIqftQcwzvPY'
# channel = client.get_channel(952302204017049613)

# Connexion à l'ENT
pronote_client = pronotepy.Client('https://0410959v.index-education.net/pronote/eleve.html',
                                  username='c.bonsigne6',
                                  password='Cycy41@@',
                                  ent=ac_orleans_tours)

# Vérification de la connexion à l'ENT
if not pronote_client.logged_in:
    print("Connexion échouée")
    exit()

# Déclaration des variables
notes = []
notes_tmp = []


def recuperer_notes():
    """Récupère toutes les notes et les stocke sous forme de liste"""
    for grade in pronote_client.current_period.grades:
        notes.append(grade.grade)


@client.event
async def on_ready():
    print('Connexion en tant que {0.user}'.format(client))
    for grade in pronote_client.current_period.grades:
        notes_tmp.append(grade.grade)


@client.event
async def on_message(message):
    if message.author == client.user:
        pass

    # Affiche toutes les notes avec la commande "!notes"
    if message.content.startswith('!notes'):
        recuperer_notes()
        message_notes = ''
        for note in notes:
            message_notes += str(note) + '\n'
        await message.channel.send(message_notes)
        message_notes = ''

    # Affiche la moyenne des notes avec la commande "!moyenne"
    # Problème : renvoie la moyenne de toutes les notes, et pas des
    # moyennes pour chaque matière
    if message.content.startswith('!moyenne'):
        recuperer_notes()
        somme_notes = 0
        nb_notes = 0
        for note in notes:
            if note == "Absent" or note == "NonNote":
                somme_notes += 0
            else:
                note = note.replace(",", ".")
                somme_notes += float(note)
                nb_notes += 1
        moyenne = somme_notes / nb_notes
        moyenne = round(moyenne, 2)
        await message.channel.send(f"Votre moyenne est : {moyenne}")


# async def change_status():
#     await client.wait_until_ready()
#     msgs = cycle(status)
#
#     while not client.is_closed:
#         current_status = next(msgs)
#         await client.change_presence(game=discord.Game(name=current_status))
#         await asyncio.sleep(5)

@tasks.loop(minutes=30)
async def task():
    channel = client.get_channel(952302204017049613)
    notes = []
    if not pronote_client.logged_in:
        await channel.send('Connexion à Pronote échouée')
    for grade in pronote_client.current_period.grades:
        notes.append(grade.grade)
    if notes != notes_tmp:
        await channel.send('Il y a une nouvelle note !')


@task.before_loop
async def task_before_loop():
    await client.wait_until_ready()

task.start()
client.run(TOKEN)
