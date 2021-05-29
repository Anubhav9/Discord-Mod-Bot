import discord
import os
from googleapiclient import discovery
import json

API_KEY = 'Enter your API Key here'
client = discord.Client()

"""

client = discord.Client()
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)
"""


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  if message.author == client.user:
    return
  clients = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)
  print(message.content)
  analyze_request = {'comment': { 'text': message.content },'requestedAttributes': {'TOXICITY': {},'INSULT':{},'FLIRTATION':{}}}

  response = clients.comments().analyze(body=analyze_request).execute()
  result=json.dumps(response, indent=2)
  result=json.loads(result)
  toxic_score=result['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']
  insult_score=result['attributeScores']['INSULT']['spanScores'][0]['score']['value']
  flirt_score=result['attributeScores']['FLIRTATION']['spanScores'][0]['score']['value']
  if(toxic_score>insult_score and toxic_score>flirt_score):
    await message.channel.send('Message Category: Toxic\nToxic Comment Detected 😡😡. Warning!')
  if(insult_score>toxic_score and insult_score>flirt_score):
    await message.channel.send('Message Category: Insult\nInsulted 🤬🤬. Do not repeat')
  if(flirt_score>toxic_score and flirt_score>insult_score):
    await message.channel.send('Message Category: Flirt\nWait! Are you flirting with me 😏😏?')
    


        

client.run('Enter your token for the bot here')