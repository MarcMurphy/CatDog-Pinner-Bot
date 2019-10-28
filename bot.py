import os
import io
import discord
import boto3
import requests
from PIL import Image
from dotenv import load_dotenv

rekognition = boto3.client('rekognition')

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    for attachment in message.attachments:
        if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.jpeg') or attachment.filename.endswith('.png'):
            imageRequest = requests.get(attachment.url)
            image = Image.open(io.BytesIO(imageRequest.content))
            stream = io.BytesIO()
            image.save(stream,format="JPEG")
            image_binary = stream.getvalue()

            response = rekognition.detect_labels(Image={'Bytes':image_binary})
            for label in response['Labels']:
                if label['Name'] == 'Cat' or label['Name'] == 'Dog':
                    await message.pin()
                    break

client.run(token)