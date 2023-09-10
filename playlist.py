# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import asyncio
import time
import discord
import re
from discord.ext import commands

import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from constants import CREDS_FILE, TOKEN_FILE

scopes = ["https://www.googleapis.com/auth/youtube"]

description = '''
            An example bot to showcase the discord.ext.commands extension module.
            There are a number of utility commands being showcased here.
            '''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

class Playlist(commands.Cog):
    def __init__(self, bot, playlist_id):
        self.bot = bot
        self.playlist_id = playlist_id
         
        # creates/saves credentials
        creds = None
        client_secrets_file = CREDS_FILE
        api_service_name = "youtube"
        api_version = "v3"
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        self.youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)

        
    @bot.command()
    async def playlist(self, ctx, playlist_link: str):
        try:
            playlist_id = playlist_link.split("=")[1].split("&")[0]
            print(playlist_id)
        except:
            return await ctx.send("Invalid youtube playlist link")
        
        title_request = self.youtube.playlists().list(
            part="snippet",
            id=playlist_id
        )
        
        items_request = self.youtube.playlists().list(
            part="contentDetails",
            id=playlist_id
        )
        
        try:
            title_response = title_request.execute()
            print(title_response)
            items_response = items_request.execute()
            print(items_response)
        except:
            return await ctx.send("Error when sending request to the youtube API")
        
        try:
            playlist_count = items_response.get('items')[0].get("contentDetails").get("itemCount")
            playlist_name = title_response.get('items')[0].get("snippet").get("title")
            await ctx.send(f"\"{playlist_name}\" has {playlist_count} videos")
        except:
            return await ctx.send("Error when getting playlist information")
            
    @bot.command()
    async def add(self, ctx, video_link: str):
        try:
            video_id = re.search(r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", video_link).group(1)
            print(video_id)
        except:
           return await ctx.send("Invalid youtube video link")
            
        add_request = self.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": self.playlist_id,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        
        try:
            add_response = add_request.execute()
            print(add_response)
        except:
            return await ctx.send("Error when sending request to the youtube API")

        try:
            video_name = add_response.get('snippet').get('title')
            await ctx.send(f"\"{video_name}\" was successfully added to the playlist!")
        except:
            return await ctx.send("Error when reading response from the youtube API")