from pytube import YouTube, Playlist ,exceptions as yte
from icecream import ic
from urllib import error as urle
from time import sleep
import os
import ffmpeg

id_dict = {
    "251": ".opus",
    "140": ".m4a",
    "401": "-2k.mp4", #2k
    "402": "-4k.mp4",  #4k
    "22": "-720p.mp4", # 720p with audio
    "247" : "-vp9-720p.vonly.mp4"
}

def progress_func(*args, **kwargs):
    print("-", end="", flush=True)


def complete_func(*args, **kwargs):
    print("\ndownload completed", flush=True)


def download_stream_id_to_file(yt: YouTube, stream_id :str) -> bool:
    """Downloads given (audio) stream (stream_id) from youtube (yt) vide0

    Args:
        yt (YouTube): a YouTube object
        stream_id (str): Which stream to download

    Returns:
        bool: Sucessfull or not Sucessfull download
    """
    
    stream = yt.streams.get_by_itag(stream_id)
    if not stream:
        print(f"unable to find stream with id [{stream_id}]")
        return False
    
    yt.register_on_progress_callback(progress_func)
    yt.register_on_complete_callback(complete_func)
    ic(stream.abr)
    ic(stream.audio_codec)
    ic(stream.bitrate)
    ic(stream.filesize_mb)
    filename = stream.default_filename.split(sep=".")[0]
    filename = renice_filename(filename)
    
    filename_w_ext = filename + id_dict.get(stream_id, ".unknown")
    print(filename_w_ext)
    
    print("Download in progress: ", end="", flush=True)
    try:
        stream.download(filename=filename_w_ext)
    except urle.HTTPError:
        return(2)
        
    VIDEO=False
    if VIDEO:
        filename_w_ext = filename + ".mp4"
        video_stream = yt.streams.filter(progressive=False, only_video=True)
        ic(video_stream)
        # video_stream.download(filename=filename_w_ext)

    return True

def renice_filename(filename):
    replace_dict = {
        " ": "_",
        "(": "",
        ")": "",
    }
    filename = "".join([replace_dict.get(c, c) for c in filename])
    filename = filename.replace("__", "_")
    filename = filename.rstrip("_")
    
    return filename

def combine_av(yt: YouTube, streams):
    stream=yt.streams.get_audio_only()
    filename = stream.default_filename.split(sep=".")[0]
    filename = renice_filename(filename)
    ic(filename)
    audioStreamToUse="251" #(opus)
    #audioStreamToUse="140" #(m4a) 
    if "251" in streams:
        audio_filename = filename + id_dict.get(audioStreamToUse, ".unknown")
        video_filename = filename + ".mp4"
        
        path=os.getcwd()
        audio_file=os.path.join(path,audio_filename)
        video_file=os.path.join(path,video_filename)
        
        input_audio = ffmpeg.input(audio_file)
        input_video = ffmpeg.input(video_file)
        output_filename = filename +"_with_audio.mp4"
        output_file=os.path.join(path,output_filename)
        check_file = os.path.isfile(output_file)
        ffmpegbin=os.path.join(path,"ffmpeg-6.1.1-essentials_build","bin","ffmpeg.exe")
        ic(input_audio)
        ic(input_video)
        ic(output_file)
        if not check_file:
            concat=ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_filename).run(cmd=ffmpegbin)
            # #ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_filename).run()
            # concatff=ffmpeg.concat(input_video, input_audio, v=1, a=1)
            # ic(concatff)
            # of=concatff.output(output_file)
            # ic(of)
            # retval=of.run()
            # ic(retval)
        else:
            print("file exists")

def handle_playlist(playListURI : str):
    pl=Playlist(playListURI)
    ic(pl)
    for vid in pl:
        get_single_yt(vid,True)    
        
        
def get_single_yt(URI :str, LQ_VIDEO=False):
    yt = YouTube(URI)
    try:
        title = yt.title
        print(f"found: {title}")

        # Stream info:
        # https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f
        formats = {
            "VideoFormats": {
                "1080p": [699, 399, 335, 303, 248, 299, 137],
                "720p": [698, 398, 334, 302, 247, 298, 136],
                "480p": [697, 397, 333, 244, 135],
                "360p": [696, 396, 332, 243, 134],
                "240p": [695, 395, 331, 242, 133],
                "144p": [694, 394, 330, 278, 160],
                "1440p": [700, 400, 336, 308, 271, 304, 264],
                "2K": [701, 401, 337, 315, 313, 305, 266],
                "4K": [402, 571, 272, 138],
            },
            "AudioFormats": {
                "AAC_LC 128Kbps": 140,
                "AAC_LC 256Kbps": 141,
                "AAC_HEv1 48Kbps": 139,
                "Opus ~50Kbps": 249,
                "Opus ~70Kbps": 250,
                "Opus <=160Kbps": 251,
                "AAC_HEv1 192Kbps": 256,
                "AAC_LC_5.1 384Kbps": 258,
                "AAC_LC_5.1 256Kbps": 327,
                "Opus ~480Kbps": 338,
            },
        }


        # 22 is 720p with audio
        # 140 is best m4a / audio only
        # 251 is best opus / audio only
        #yt = YouTube(URI)
        #st=yt.streams.filter(progressive=True)
        #print(st)
        #exit()
        
        HQ_VIDEO = False
        
        LQ_AUDIO_VIDEO = False
        VIDEO_720p= False
        
        streams = ['140', '251']  
        if LQ_AUDIO_VIDEO:
            streams.append("22")
        if VIDEO_720p:
            streams.append("247")
        if HQ_VIDEO:
            streams.append("401")
        for stream_id in streams:            
            retval= download_stream_id_to_file(yt, stream_id)
            while retval == 2:
                yt = YouTube(URI)
                retval= download_stream_id_to_file(yt, stream_id)
                yt.streams.filter(progressive=True)
        
        #if HQ_VIDEO:
        #    combine_av(yt,streams)

    except yte.VideoUnavailable:
        print(f"Unable to find {URI}")

def list_streams(URI: str):
    yt = YouTube(URI)
    
    ic(URI)
    ic(YouTube)
    
    streams=yt.streams
    for stream in streams:
        ic(stream)    

if __name__ == "__main__":

    URI = ""
    
    playlist=''
    
    if URI:
        list_streams(URI)
        get_single_yt(URI)
    if playlist:
        handle_playlist(playlist)