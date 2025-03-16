import tkinter.filedialog
import tkinter as tk
import pytube
import os
import re

#------------------------------------------------------------------------------    
###---------------------------DEFAULT VALUES--------------------------------###
#------------------------------------------------------------------------------


default_rep= "/home/admin/Downloads" #default DL folder
rep = default_rep #rep where DL will take place (either default or user chosen)
chosen_rep = rep #rep chosen by user in case a diff one is chosen
resolution="720p" #default res
media_type="video" #default media type when downloading
playlist_resolution="highest" #default resolution for playlists
playlist_on=0 #if chosen playlist or not !!!DONT CHANGE!!!
max_resolution_playlist = "1080p" #choose 









#------------------------------------------------------------------------------    
###------------------------------FUNCTIONS----------------------------------###
#------------------------------------------------------------------------------







def explore():
    global rep, chosen_rep
    chosen_rep = tk.filedialog.askdirectory()
    rep = chosen_rep 
    print("directory: ", rep)


def default_values():
    if media_type=="video":
        resolution="720p"
        #Change message
        message1="Resolution: " 
        message= message1+resolution
        text.config(text= message)
    else:
        resolution="128kbps" #set new default resolution
        #Change message
        message1="Resolution: " 
        message= message1+resolution
        text.config(text= message)


#FUNCTION ASSOCIATTED WITH VIDEO BUTTON
def video():
    global media_type, resolution
    media_type="video"
    
    #Change button look
    button_video.config(relief=tk.SUNKEN)
    button_audio.config(relief=tk.RAISED)
    
    if playlist_on==0: 
        resolution="360p"
        #Change message
        message1="Resolution: " 
        message= message1+resolution
        text.config(text= message)
        
    #Close resolution window
    newWindow.destroy()


#FUNCTION ASSOCIATED WITH AUDIO BUTTON
def audio():
    global media_type, resolution
    media_type="audio"

    #Change button look
    button_audio.config(relief=tk.SUNKEN)
    button_video.config(relief=tk.RAISED)

    if playlist_on==0:
        resolution="128kbps" #set new default resolution
        #Change message
        message1="Resolution: " 
        message= message1+resolution
        text.config(text= message)


    #Close resolution window
    newWindow.destroy()


    
#FUNCTION ASSOCIATED WITH PLAYLIST BUTTON   
def playlist(url):
    global newWindow, playlist_resolution, playlist_on
    
    if playlist_on==0:
        button_playlist.config(relief=tk.SUNKEN)#modify button look
        playlist_on=1 #mode playlist activated
        #modify resolution text
        message1="Resolution: " 
        message= message1+playlist_resolution
        text.config(text= message)
    else:
        button_playlist.config(relief=tk.RAISED)#modify button look
        playlist_on=0 #mode playlist canceled
    default_values()
            
    #Close resolution window
    newWindow.destroy()



#FUNCTION ASSOCIATED WITH QUALITY BUTTON    
def quality(url):
    global playlist_on
    print(playlist_on)
    if playlist_on==0:
        quality_normal(url)
    else:
        quality_playlist(url)








###----------------------###
#  THE QUALITY FUNCTIONS   #
###----------------------###








def sort_list(streams):  #it works but I have no idea how I copied it off thh internet 
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    streams.sort(key=alphanum)
    return streams


#Quality choice when not a playlist
def quality_normal(url):
    global button_label_list, streams, media_type, newWindow
    try:
        if newWindow.state() == 'normal':
            print("window quality already open wtf you doing boi")
    except:
        yt = pytube.YouTube(url)  
        streams = set()

        if media_type=="audio":
        #For audio
            for stream in yt.streams.filter(type="audio"):  
                streams.add(stream.abr)
        else:
        #For videos
            for stream in yt.streams.filter(mime_type="video/mp4"):  
                streams.add(stream.resolution)

        streams= list(streams)
        streams = sort_list(streams)
        print(streams)
    
    #Check if a window already is open before opening a new one: 
    #check if open
        #create new window
        newWindow= tk.Toplevel(root)
        newWindow.title("Choose Quality")

        #number of buttons to create:
        num =len(streams)
        print(num)

        #creating the buttons
        for i in range(num):
            button = tk.Button(newWindow, text=streams[i], command=lambda x=i: get_res(x))
            if media_type=="audio":
                if i < 4:
                    button.place(relx=0.01+i*0.24, rely=0.20, relwidth=0.23)
                    print("i=", i)
                else: 
                    button.place(relx=0.01+(i-3)*0.24, rely=0.50, relwidth=0.23)
                    print("i:", i)
            else:
                button.place(relx=0.01+i*0.16, rely=0.50, relwidth=0.15)

#Baby function of quality_normal()
def get_res(i):
    global resolution, newWindow
    resolution=streams[i]
    print("resolution choisis: ", resolution)
    
    #Show chosen resolution in GUI

    message1="Resolution: " 
    message= message1+resolution
    text.config(text= message)

    #Close resolution window
    newWindow.destroy()




#Quality choice when working with a playlist
def quality_playlist(url):
    global newWindow
    #create new window
    newWindow= tk.Toplevel(root)
    newWindow.title("Choose Quality")

    #the buttons
    button = tk.Button(newWindow, text="highest", command=lambda : get_res_playlist("highest"))
    button.place(relx=0.2, rely=0.10, relwidth=0.55)

    button = tk.Button(newWindow, text="medium", command=lambda : get_res_playlist("medium"))
    button.place(relx=0.2, rely=0.25, relwidth=0.55)

    button = tk.Button(newWindow, text="lowest", command=lambda : get_res_playlist("lowest"))
    button.place(relx=0.2, rely=0.40, relwidth=0.55)

#Baby function of quality_playlist    
def get_res_playlist(quality):
    global playlist_resolution, newWindow
    playlist_resolution = quality

    #Show chosen resolution in GUI
    message1="Resolution: " 
    message= message1+quality
    text.config(text= message)
    newWindow.destroy()




#Functions that find the highest, medium or lowest qualities
def list_resolution(media):
    global media_type
    streams = set()
    if media_type=="audio":
        #For audio
        for stream in media.streams.filter(type="audio"):  
            streams.add(stream.abr)
    else:
        #For videos
        for stream in media.streams.filter(mime_type="video/mp4"):  
            streams.add(stream.resolution)

    streams= list(streams)
    streams = sort_list(streams)
    print(streams)

    return streams

def download_lowest():
    default_values()

def download_medium(media):
    global resolution
    #list resolutions 
    res_list = list_resolution(media)

    #find medium resolution 
    len_res_list= len(res_list)
    if (len_res_list % 2) == 0:
        #if number even: 
        resolution = res_list[int(len_res_list/2)]
    else: 
        #if odd number
        resolution = res_list[int((len_res_list+1)/2)]
    print("resolution chosen", resolution)

def download_highest(media):
    global resolution, max_resolution_playlist
    res_list = list_resolution(media)
    
    #check if max_resolution in in the list
    if max_resolution_playlist in res_list:
        resolution = max_resolution_playlist
    else: 
        resolution = res_list[-1]
    print("resolution chosen", resolution)






###------------------------###
#   THE DONWLOAD FUNCTIONS   #
###------------------------###





##FUNCTION ASSOCIATED WITH PLAYLIST BUTTON  
def download(url):
    global media_type, resolution
    yt = pytube.YouTube(url)

    if playlist_on ==1 :
        download_playlist(url)
    else:
        download_media(yt)




def make_playlist_folder(playlist):
    global rep
    playlist_title = playlist.title.replace(":", "-")
    playlist_folder = rep+"/"+ playlist_title
    playlist_folder = playlist_folder
    os.mkdir(playlist_folder)
    rep = playlist_folder



def download_playlist(url):
    global media_type, playlist_resolution, rep
    playlist = pytube.Playlist(url)

    #make playlist folder
    ''' you can remove this part of the code if you want'''
    make_playlist_folder(playlist)
    #

    #loop pour qualité et download
    for video in playlist.videos:
        #qualité
        if playlist_resolution == "lowest":
            download_lowest()
        if playlist_resolution == "medium":
            download_medium(video)
        if playlist_resolution == "highest":
            download_highest(video)
        #download
        download_media(video)
    
    rep=chosen_rep



def download_media(yt):
    global rep, media_type, resolution 
    #download audio 
    if media_type=="audio":
        stream = yt.streams.filter(only_audio=True).filter(abr=resolution).first()
        #change filename for audio to make it a .mp3
        audioname=yt.streams.first().default_filename[:-4]+'.mp3'
        stream.download(rep, filename=audioname)

    #download video    
    else:
        if resolution=="360p":
            video = yt.streams.filter(res=resolution).first()
            video.download(rep)
                        
    #if good quality video has to download audio and video seperately
        else:
            #make new folder
            new_folder_name = rep+"/"+yt.streams.first().default_filename[:-4]
            os.mkdir(new_folder_name)
            #change filename for audio to make it a .mp3
            audioname=yt.streams.first().default_filename[:-4]+'.mp3'
            #download audio
            stream = yt.streams.filter(only_audio=True, abr="128kbps").first()
            stream.download(new_folder_name, filename=audioname)
            #download video
            video = yt.streams.filter(res=resolution).first()
            video.download(new_folder_name)

   
                
            





#------------------------------------------------------------------------------    
###---------------------------------GUI-------------------------------------###
#------------------------------------------------------------------------------





#Partie Graphic User Interface 
root=tk.Tk()

#window
canvas=tk.Canvas(root, height=100000000 ,width=1000)
canvas.place()

#entré pour mettre URL
entry = tk.Entry(root)
entry.insert(0, 'enter video url')
entry.place(relx=0.2, rely=0.10, relwidth=0.55)

#creation bouton audio et vidéo
button_audio = tk.Button(root, text="audio", command=lambda: audio(), bg="light sky blue")
button_audio.place(relx=0.2, rely=0.25, relwidth=0.25)

button_video = tk.Button(root, text="video", command=lambda: video(), bg="light sky blue")
button_video.place(relx=0.5, rely=0.25, relwidth=0.25)
button_video.config(relief=tk.SUNKEN)

#playlist
button_playlist = tk.Button(root, text="Playlist", command=lambda: playlist(entry.get()))
button_playlist.place(relx=0.2, rely=0.40, relwidth=0.55)


#choisir la qualité
button = tk.Button(root, text="Change quality", command=lambda: quality(entry.get()))
button.place(relx=0.2, rely=0.55, relwidth=0.55)

#text info sur la qualité
text = tk.Label(root, text= "resolution : 360p")
text.place(relx=0.2, rely=0.70, relwidth=0.55)

#choose file
choose= tk.Button(root, text="Choose directory", command=explore)
choose.place(relx=0.2, rely=0.83, relwidth=0.55)

#download
button = tk.Button(root, text="Download", command=lambda: download(entry.get()), bg="green")
button.place(relx=0.2, rely=0.98, relwidth=0.55)

#text.pack()
root.mainloop()