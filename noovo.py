#import requests
#
#
#def requesting(url):
#    response = requests.get(url)
#
#    try:
#        return response.json()
#    except:
#        return response.text
#
#
#
#id = 2518860
#info_url = f"https://capi.9c9media.com/destinations/canald_hub/platforms/desktop/contents/{id}?$lang=fr&$include=[Desc,Type,Media,Images,ContentPackages,Authentication,Season,ChannelAffiliate,Owner,RevShare,AdTarget,Keywords,AdRights,Tags]"
#info_resp = requesting(info_url)
#try:
#    info = f"{info_resp["Media"]["Name"]} - {info_resp["Name"]}"
#    print(info)
#except:
#    pass
#
#contents_url = f"https://capi.9c9media.com/destinations/canald_hub/platforms/desktop/contents/{id}/contentPackages?$lang=fr"
#contents_resp = requesting(contents_url)
#
#try:
#    second_id = contents_resp["Items"][0]["Id"]
#    print(id)
#    print(second_id)
#    to_mpd_url = f"https://capi.9c9media.com/destinations/canald_hub/platforms/tvos/playback/contents/{id}/contentPackages/{second_id}/manifest.mpd?action=reference&ssl=true&filter=fe&mca=true&uhd=true&mcv=true&hd=true&tpt=true&mta=true&stt=true"
#    mpd_url = requesting(to_mpd_url)
#    subs_mpd_url = mpd_url.replace("zbest", "zultimate")
#    print(subs_mpd_url)
#    print()
#except:
#    pass

import requests
import json
import noovo_tools




#response = requests.post(url=url, data=json.dumps(noovo_tools.search_body(query)))
#print("response status code: ", response.status_code)
#if response.status_code == 200:
#    print("response : ", response.content)



import sys
import tools
import subprocess
import dash
import bell_tokens


def search_shows(query: str, quiet: bool = False) -> None:
    
    url, body = noovo_tools.search_body(query)

    resp = requests.post(url, data=json.dumps(body)).json()
    
    results: list[dict[str, str]] = []

    shows = resp["data"]["searchResults"]["page"]["items"]

    for show in shows:
        results.append({show["path"]: show["title"]})
        
        if not quiet:
            print(f"{show["title"]} | {show["path"]}\n{show["summary"]}\n")

    return results




def list_episodes(show_path: str, quiet: bool = False) -> dict[str, str]:
    if not noovo_tools.validate_url(show_path):
        shows_path = search_shows(show_path, quiet)
        for key in shows_path[0].keys():
            show_path = key
    


    req_url, headers = noovo_tools.show_path_url(show_path)
    
    resp = {"errors": {}}
    while "errors" in resp.keys():
        resp = requests.get(req_url, headers=headers).json()

    with open("file.json", "wt") as f:
        f.write(json.dumps(resp))

    if resp["data"]["resolvedPath"]["segments"][1]["content"]["__typename"] != "AxisMedia":
        return
    
    show_id = resp["data"]["resolvedPath"]["segments"][1]["content"]["id"]
    
    req_url, headers = noovo_tools.show_id_url(show_id, show_path)

    resp = {"errors": {}}
    while "errors" in resp.keys():
        resp = requests.get(req_url, headers=headers).json()

    with open("file.json", "wt") as f:
        f.write(json.dumps(resp))

    show = get_show_info(resp)
    
    if not quiet:
        print(show["title"])
        print("-----------------------------------------------------------------------------------------------------")
        print(show["description"])
        print("-----------------------------------------------------------------------------------------------------")
        for show_genre in show["genres"]:
            print(show_genre)
        print("-----------------------------------------------------------------------------------------------------")

    if show["mediaType"] == "SERIES":

        show["episodes"] = []

        for season in show["seasons"]:

            req_url, headers, body = noovo_tools.season_id_url(season["id"], show_path)

            resp = requests.post(req_url, headers=headers, data=json.dumps(body)).json()

            with open("file.json", "wt") as f:
                f.write(json.dumps(resp))

            for episode in resp["data"]["axisSeason"]["episodes"]:

                with open("file.json", "wt") as f:
                    f.write(json.dumps(episode))

                #req_url, headers, body  = noovo_tools.episode_id_url(episode["id"])
                #
                #curl_command = f"curl '{req_url}' --compressed -X POST"
                #for shit1, shit2 in headers.items():
                #    curl_command += f" -H '{shit1}: {shit2}'"
                #curl_command += f" --data-raw '{json.dumps(body)}'"
                #print(curl_command)
                #
                #resp = requests.post(req_url, headers=headers, data=json.dumps(body)).json()
                #
                #with open("file.json", "wt") as f:
                #    f.write(json.dumps(resp))

                episode_info = get_episodes_info(episode)
                episode_info["seasonNumber"] = season["seasonNumber"]
                episode_info["seasonTitle"] = season["title"]

                show["episodes"].append(episode_info)

                if not quiet:
                    print(f"{episode["path"]} - {season["title"]} - {episode["title"]}")

        return show
    
    else:
        show["episodes"] = []

        for episode in show["episode"]:
            with open("file.json", "wt") as f:
                f.write(json.dumps(episode))
            
            episode_info = get_episodes_info(episode)
            episode_info["seasonNumber"] = 0
            episode_info["seasonTitle"] = episode["title"]

            show["episodes"].append(episode_info)

            print(f"{episode["path"]} - {show["title"]} - {episode["title"]}")
    
    return show




def get_show_info(resp):
    show: dict[str, str] = {}
    show["title"] = resp["data"]["contentData"]["title"]
    show["mediaType"] = resp["data"]["contentData"]["mediaType"]
    #show["requestedType"] = resp["data"]["contentData"]["requestedType"]
    #show["country"] = resp["data"]["contentData"]["structuredMetadata"]["countryOfOrigin"]["name"]
    show["language"] = resp["data"]["contentData"]["normalizedRatingCodes"][0]["language"]
    show["description"] = resp["data"]["contentData"]["description"]
    #show["type"] = resp["data"]["contentData"]
    #show["numberOfEpisodes"] = resp["data"]["contentData"]

    
    if show["mediaType"] == "SERIES":
        show["seasons"] = []
        for season in resp["data"]["contentData"]["seasons"]:
            show["seasons"].append({"title": season["title"], "id": season["id"], "seasonNumber": season["seasonNumber"]})
        
    else:
        show["episode"] = []
        for episode in resp["data"]["contentData"]["mainContents"]["page"]["items"]:
            show["episode"].append(episode)


    show["genres"] = []

    for show_genre in resp["data"]["contentData"]["genres"]:
        show["genres"].append(show_genre["name"])
    
    return show


def get_episodes_info(episode):
    episode_info = {}

    episode_info["id"] = episode["id"]
    episode_info["title"] = episode["title"]
    episode_info["duration"] = episode["duration"]

    try:
        episode_info["description"] = episode["description"]
    except:
        episode_info["description"] = episode["summary"]
    
    episode_info["episodeNumber"] = episode["episodeNumber"]
    #episode_info["contentType"] = episode["contentType"]

    return episode_info



def get_chosen_episodes(all_episodes, url, start_season, end_season, start_episode, end_episode, allow_trailers, quiet):
    chosen_episodes = show_info(url, quiet)
    chosen_episodes["episodes"] = []

    for episode in all_episodes["episodes"]:
        if int(episode["seasonNumber"]) < start_season:
            continue
        if int(episode["seasonNumber"]) > end_season:
            break
        if int(episode["seasonNumber"]) == end_season and int(episode["episodeNumber"]) > end_episode:
            break
        if int(episode["seasonNumber"]) <= start_season and int(episode["episodeNumber"]) < start_episode:
            continue
        
        #if episode["mediaType"] != "Trailer" or allow_trailers:
        chosen_episodes["episodes"].append(episode)
    
    return chosen_episodes
        
        


def show_info(show_path: str, quiet: bool = False) -> dict[str, str]:
    if not noovo_tools.validate_url(show_path):
        shows_path = search_shows(show_path, quiet)
        for key in shows_path[0].keys():
            show_path = key


    req_url, headers = noovo_tools.show_path_url(show_path)
    
    resp = {"errors": {}}
    while "errors" in resp.keys():
        resp = requests.get(req_url, headers=headers).json()

    with open("file.json", "wt") as f:
        f.write(json.dumps(resp))

    if resp["data"]["resolvedPath"]["segments"][1]["content"]["__typename"] != "AxisMedia":
        return
    
    show_id = resp["data"]["resolvedPath"]["segments"][1]["content"]["id"]
    
    req_url, headers = noovo_tools.show_id_url(show_id, show_path)

    resp = {"errors": {}}
    while "errors" in resp.keys():
        resp = requests.get(req_url, headers=headers).json()

    with open("file.json", "wt") as f:
        f.write(json.dumps(resp))

    show = get_show_info(resp)
    
    if not quiet:
        print(show["title"])
        print("-----------------------------------------------------------------------------------------------------")
        print(show["description"])
        print("-----------------------------------------------------------------------------------------------------")
        for show_genre in show["genres"]:
            print(show_genre)
        #print("-----------------------------------------------------------------------------------------------------")
        #print(f"{show["numberOfSeasons"]} saisons")
        #print(f"{show["numberOfEpisodes"]} episodes")
        print("-----------------------------------------------------------------------------------------------------")
        print(show["mediaType"])

    return show


def get_download(url, latest, seasons_episodes, options):
    url, start_season, end_season, start_episode, end_episode = tools.parse_season_episode(url, seasons_episodes)
    all_episodes = list_episodes(url, options["quiet"])

    chosen_episodes = {}
    
    if latest:
        chosen_episodes = show_info(url, options["quiet"])
        chosen_episodes["episodes"] = all_episodes["episodes"][-1:]
    
    else:
        chosen_episodes = get_chosen_episodes(all_episodes, url, start_season, end_season, start_episode, end_episode, options["allow_trailers"], options["quiet"])
    
    options["language"] = chosen_episodes["language"]

    options["headers"], options["wvd_path"], custom_string = connect()
    
    #Loops through all the chosen episodes and downloads them all
    for episode in chosen_episodes["episodes"]:
        options["clean_name"] = chosen_episodes["title"]

        if episode["seasonNumber"] == 0 and episode["episodeNumber"] == 0:
            options["clean_name"] = chosen_episodes["title"]
            options["path"] = f'{chosen_episodes["titre"]}'
        
        else:
            options["path"] = f'{chosen_episodes["title"]}.S{episode["seasonNumber"]:02}E{episode["episodeNumber"]:02}.{options["language"].upper()[:2]}'
            options["clean_name"] = f'{chosen_episodes["title"]} Saison {episode["seasonNumber"]} Episode {episode["episodeNumber"]}'

        if options["all_audios"]:
            options["path"] += ".AD"
        
        options["path"] += f'.{options["resolution"]}p{custom_string}'

        download_content(episode["id"], options)


def download_content(id: int, options):
    episode_info_url, headers, body = noovo_tools.episode_id_url(id)

    #curl_command = "curl -X POST"

    r = requests.post(episode_info_url, headers=headers, data=body)
    resp = r.json()
    
    if r.status_code != 200:
        return

    if resp["errorCode"] != 0:
        r = requests.get(url=episode_info_url, headers=options["headers"])
        resp: dict[str, str] = r.json()
    
    if r.status_code != 200:
        return

    #fixed_resp = tools.fix_json(resp)

    low_res_mpd = fixed_resp["url"]
    mpd_url: str = low_res_mpd.replace("filter=3000", "filter=7000")
    key: str = fixed_resp["widevineAuthToken"]
    licence_url: str = fixed_resp["widevineLicenseUrl"]

    headers = {"x-dt-auth-token": key}

    options["mpd_url"] = mpd_url
    options["licence_url"] = licence_url
    options["headers"] = headers

    

    return download_toutv(options)

def download_toutv(options):

    options["pssh"] = dash.get_pssh(options["mpd_url"], options["quiet"])

    options["decryption_keys"] = dash.setup_licence_challenge(options["pssh"], options["licence_url"], options["wvd_path"], options["headers"])

    n_m3u8dl_re_command = [
        "n-m3u8dl-re",
        options["mpd_url"],
        "-mt",
        "--mp4-real-time-decryption",
        "--use-shaka-packager",
        "-sv",
        f"res={options["resolution"]}*",
        "--save-name",
        options["path"]
    ]

    for key in options["decryption_keys"]:
        n_m3u8dl_re_command.append("--key")
        n_m3u8dl_re_command.append(key)

    if options["all_audios"]:
        n_m3u8dl_re_command.append("-sa")
        n_m3u8dl_re_command.append("all")
    else:
        n_m3u8dl_re_command.append("-sa")
        n_m3u8dl_re_command.append("best")
    
    if options["subs"]:
        n_m3u8dl_re_command.append("--sub-format")
        n_m3u8dl_re_command.append("VTT")
        n_m3u8dl_re_command.append("-ss")
        n_m3u8dl_re_command.append("all")


    if options["quiet"]:
        subprocess.run(n_m3u8dl_re_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(n_m3u8dl_re_command)

    mkvmerge_command = [
        "mkvmerge",
        "-o",
        f"{options["path"]}.mkv",
        "--title",
        options["clean_name"],
        "--default-language",
        options["language"]
    ]

    audio_1 = tools.get_downloaded_name(options["path"], ".m4a", [])

    if options["all_audios"]:
        audio_2 = tools.get_downloaded_name(options["path"], ".copy.m4a", [audio_1[0]])
    
    if options["subs"]:
        subs = tools.get_downloaded_name(options["path"], ".vtt", [])

    if options["quiet"]:
        mkvmerge_command.append("-q")
    else:
        mkvmerge_command.append("-v")

    track_name = options["language"]

    if options["language"] == "fr-CA":
        track_name = "VFQ"
    
    #VIDEO
    mkvmerge_command.extend(["--original-flag", "0", "--default-track-flag", "0", "--track-name", f"0:original {options["resolution"]}p", f"{options["path"]}.mp4"])

    #AUDIO
    mkvmerge_command.extend(["--original-flag", "0", "--default-track-flag", "0", "--language", f"0:{options["language"]}", "--track-name", f"0:{track_name}", audio_1[0]])
    
    if options["all_audios"]:
        #AUDIODESCRIPTION
        mkvmerge_command.extend(["--visual-impaired-flag", "1", "--default-track-flag", "0:0", "--language", f"0:{options["language"]}", "--track-name", f"0:{track_name} AD", audio_2[0]])

    if options["subs"]:
        if subs != []:
            mkvmerge_command.extend(["--language", f"0:{options["language"]}", "--track-name", f"0:{track_name} ", subs])

    if options["quiet"]:
        subprocess.run(mkvmerge_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(mkvmerge_command)
    
    tools.delete_files(options["path"], [".mkv"])


def help():
    print(noovo_tools.help_text)
    exit()

def connect():
    settings_path = "settings.json"

    return(bell_tokens.login(settings_path, "noovo"))

def search(args):
    if len(args) > 2:
        return(search_shows(args[2]))
    else:
        return(search_shows(""))


def list(args):
    if len(args) > 2:
        return list_episodes(args[2])

def info(args):
    if len(args) > 2:
        if not noovo_tools.validate_url(args[2]):
            url = search_shows(args[2])
            for key in url[0].keys():
                url = key
            return show_info(url)
    

def download(args):

        resolution = 1080
        quiet = False
        audiodescription = False
        allow_trailers = False
        latest = False
        subs = False


        if "-r" in args:
            resolution = args[int(args.index("-r") + 1)]
        if "-q" in args:
            quiet = True
        if "-ad" in args:
            audiodescription = True
        if "-t" in args:
            allow_trailers = True
        if "-l" in args:
            latest = True
        if "-s" in args:
            subs = True
        
        seasons_episodes = ""
        if len(args) > 3:
            if args[3][1:] != "-":
                seasons_episodes = args[3]
        
        url = args[2]
        if len(args) > 2:
            if not noovo_tools.validate_url(url):
                url = search_shows(url, quiet)
                for key in url[0].keys():
                    url = key
        
        options = {
            "resolution": resolution,
            "quiet": quiet,
            "all_audios": audiodescription,
            "allow_trailers": allow_trailers,
            "subs": subs
        }
        
        get_download(url, latest, seasons_episodes, options)



            

args = sys.argv

#if len(args) < 2:
#    print(noovo_tools.help_text)
#    if "download" == "download":
#        args.append("download")
#        args.append("completement lycee")
#        #args.append("-l")
#        #args.append("-s")
#        #args.append("-q")
#
#        download(args)
#
#    exit()

#if args[1] == "help":
#    help()



#if args[1] == "connect":
#    connect()


#if args[1] == "search":
#    args.append("search")
#    args.append("completement")
#    search(args)



#if args[1] == "list":
#    args.append("list")
#    #args.append("completement")
#    args.append("emmerdeur")
#
#    list(args)
#    
#
#
#if args[1] == "info":
#    args.append("list")
#    args.append("completement")
#    args.append("emmerdeur")
#    info(args)
#
#if args[1] == "download":
if "download" == "download":

    args.append("download")
    args.append("lycee")
    #args.append("-r")
    #args.append("720")
    #args.append("-ad")
    #args.append("s1-s3")

    download(args)
#