# HANDLES GETTING MUSIC FILES

import glob
import os
import pytube
import discord


def getVideo(args):

    # Try to get playlist from link
    playlistCheck = args[0].split('&')[-1][0:5]
    print(playlistCheck)
    if playlistCheck == "index":
        try:
            return pytube.Playlist(args[0]).videos
        except:
            pass

    # Try to get video from link
    try:
        return [pytube.YouTube(args[0])]
    except:
        pass

    # Try to get video from search terms
    try:
        return [pytube.Search(' '.join(args)).results[0]]
    except:
        pass

    return None

async def queueManager(ctx, musicDict):
    pass


def getYTFile(video, id):
    t = video.streams.filter(only_audio=True)
    #print(t)
    t[0].download(output_path="Audio", filename=str(id) + ".mp4")
