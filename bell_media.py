import sys
import tools
import dash
import bell_tokens
import crave_tools
import noovo_tools
import requests



class Bell_Media:
    settings_path = "settings.json"
    service: str = "noovo"
    tool = noovo_tools

    def search_shows(self, query: str, quiet: bool = False):

        resp = self.tool.search_body(query)
        
        results: list[dict[str, str]] = []
    
        shows = {}
    
        if self.service == "crave":
            shows = resp["data"]["resolvedPath"]["searchResults"]["page"]["items"]
        if self.service == "noovo":
            shows = resp["data"]["searchResults"]["page"]["items"]
        
    
        for show in shows:
            results.append(show)
            
            if not quiet:
                print(f'{show["title"]} | {show["path"]}\n{show["summary"]}\n')
    
        return results
    
    
    
    
    def list_episodes(self, show: dict[str, str], quiet: bool = False) -> dict[str, str]:

        resp = self.tool.show_path_url(show["path"]).json()
        
        show_id = ""
        if "errors" in resp:
            show_id = show["id"]
        else:
            show_id = resp["data"]["resolvedPath"]["lastSegment"]["content"]["id"]
        
        resp = self.tool.show_id_url(show_id)
        
        show = self.get_show_info(resp)
        
        if not quiet:
            print(show["title"])
            print("-----------------------------------------------------------------------------------------------------")
            print(show["description"])
            print("-----------------------------------------------------------------------------------------------------")
            for show_genre in show["genres"]:
                print(show_genre)
            print("-----------------------------------------------------------------------------------------------------")

        show["episodes"] = []

        if show["mediaType"] == "SERIES":
            if len(show["seasons"]) > 1:
                if show["seasons"][0]["seasonNumber"] > show["seasons"][1]["seasonNumber"]:
                    if self.service == "crave":
                        for season in reversed(show["seasons"]):
                            show["episodes"].extend(self.go_through_season(season, quiet))
                    if self.service == "noovo":
                        for season in reversed(show["seasons"]):
                            show["episodes"].extend(self.go_through_season(season, quiet))
                else:
                    if self.service == "crave":
                        for season in show["seasons"]:
                            show["episodes"].extend(self.go_through_season(season, quiet))
                    if self.service == "noovo":
                        for season in show["seasons"]:
                            show["episodes"].extend(self.go_through_season(season, quiet))
            else:
                if self.service == "crave":
                    for season in show["seasons"]:
                        show["episodes"].extend(self.go_through_season(season, quiet))
                if self.service == "noovo":
                    for season in show["seasons"]:
                        show["episodes"].extend(self.go_through_season(season, quiet))
        
        else:
            for episode in resp["data"]["contentData"]["mainContents"]["page"]["items"]:
                episode_info = self.get_episodes_info(episode)
                episode_info["seasonNumber"] = episode["seasonNumber"]
                episode_info["seasonTitle"] = episode["title"]
    
                show["episodes"].append(episode_info)
                #show["episodes"].append(episode)

                if not quiet:
                    print(f'{episode["path"]} - {episode["title"]}')
    
    
        show["genres"] = []
    
        for show_genre in resp["data"]["contentData"]["genres"]:
            show["genres"].append(show_genre["name"])
        
        return show
    
    
    def go_through_season(self, season, quiet):

        resp = self.tool.season_id_url(season["id"])
        
        episodes = []

        if len(resp["data"]["axisSeason"]["episodes"]) > 1:
            if resp["data"]["axisSeason"]["episodes"][0]["episodeNumber"] > resp["data"]["axisSeason"]["episodes"][1]["episodeNumber"]:
                for episode in reversed(resp["data"]["axisSeason"]["episodes"]):
                
                    episode_info = self.get_episodes_info(episode)
                    episode_info["seasonNumber"] = season["seasonNumber"]
                    episode_info["seasonTitle"] = season["title"]
                    #episode_info[""]

                    episodes.append(episode_info)

                    if not quiet:
                        print(f'{episode["path"]} - {season["title"]} - {episode["title"]}')
            
            else:
                for episode in resp["data"]["axisSeason"]["episodes"]:
                
                    episode_info = self.get_episodes_info(episode)
                    episode_info["seasonNumber"] = season["seasonNumber"]
                    episode_info["seasonTitle"] = season["title"]
                    #episode_info[""]

                    episodes.append(episode_info)

                    if not quiet:
                        print(f'{episode["path"]} - {season["title"]} - {episode["title"]}')

        else:
            for episode in resp["data"]["axisSeason"]["episodes"]:
            
                episode_info = self.get_episodes_info(episode)
                episode_info["seasonNumber"] = season["seasonNumber"]
                episode_info["seasonTitle"] = season["title"]
                #episode_info[""]

                episodes.append(episode_info)

                if not quiet:
                    print(f'{episode["path"]} - {season["title"]} - {episode["title"]}')
    
        return episodes
    
    
    
    def get_show_info(self, resp):
        show: dict[str, str] = {}
        show["title"] = resp["data"]["contentData"]["title"]
        show["mediaType"] = resp["data"]["contentData"]["mediaType"]
        #show["requestedType"] = resp["data"]["contentData"]["requestedType"]
        #show["country"] = resp["data"]["contentData"]["structuredMetadata"]["countryOfOrigin"]["name"]
        show["language"] = resp["data"]["contentData"]["originalSpokenLanguage"]
        show["description"] = resp["data"]["contentData"]["description"]
        show["releaseYear"] = resp["data"]["contentData"]["firstAirYear"]
        #show["type"] = resp["data"]["contentData"]
        #show["numberOfEpisodes"] = resp["data"]["contentData"]
    
        
        if show["mediaType"] == "SERIES":
            show["seasons"] = []
            for season in resp["data"]["contentData"]["seasons"]:
                show["seasons"].append({"title": season["title"], "id": season["id"], "seasonNumber": season["seasonNumber"]})
            
        else:
            show["episodes"] = []
            for episode in resp["data"]["contentData"]["mainContents"]["page"]["items"]:
                show["episodes"].append(episode)
    
    
        show["genres"] = []
    
        for show_genre in resp["data"]["contentData"]["genres"]:
            show["genres"].append(show_genre["name"])
        
        return show
    
    
    def get_episodes_info(self, episode):
        episode_info = {}
    
        episode_info["id"] = episode["id"]
        episode_info["axisId"] = episode["axisId"]
        episode_info["title"] = episode["title"]
        episode_info["duration"] = episode["duration"]
        #episode_info["contentType"] = episode["contentType"]
        #episode_info["destinationCode"] = episode["authConstraints"][0]["packageName"]

        # NEED TO WORK ON THIS, I CAN FIND IT

        if self.service == "crave":
            episode_info["destinationCode"] = "crave_atexace_avod"
        if self.service == "noovo":
            episode_info["destinationCode"] = "noovo_hub"
    
        try:
            episode_info["description"] = episode["description"]
        except:
            episode_info["description"] = episode["summary"]
        
        episode_info["episodeNumber"] = episode["episodeNumber"]

        #episode_info["contentType"] = episode["contentType"]
    
        return episode_info
    
    
    
    def get_chosen_episodes(self, all_episodes, show, start_season, end_season, start_episode, end_episode, allow_trailers, quiet):
        chosen_episodes = self.show_info(show, quiet)
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

    
    def show_info(self, show: str, quiet: bool = False) -> dict[str, str]:

        resp = self.tool.show_path_url(show["path"]).json()
        
        show_id = ""
        if "errors" in resp:
            show_id = show["id"]
        else:
            show_id = resp["data"]["resolvedPath"]["segments"][1]["content"]["id"]
        
        resp = self.tool.show_id_url(show_id)
    
        show = self.get_show_info(resp)
        
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
    
    
    def get_download(self, show, latest, seasons_episodes, options):
        start_season, end_season, start_episode, end_episode = tools.parse_season_episode(seasons_episodes)
        all_episodes = self.list_episodes(show, options["quiet"])
    
        chosen_episodes = {}
        
        if latest:
            chosen_episodes = self.show_info(show, options["quiet"])
            chosen_episodes["episodes"] = all_episodes["episodes"][-1:]
        
        else:
            chosen_episodes = self.get_chosen_episodes(all_episodes, show, start_season, end_season, start_episode, end_episode, options["allow_trailers"], options["quiet"])
        
        options["language"] = chosen_episodes["language"]
    
        options["headers"], options["wvd_path"], custom_string = self.connect()
        
        #Loops through all the chosen episodes and downloads them all
        for episode in chosen_episodes["episodes"]:
            options["clean_name"] = chosen_episodes["title"]

            if self.service == "crave":
                episode_info_resp = self.tool.episode_id_url(episode["axisId"], service_hub_name)
                options["language"] = episode_info_resp["SpokenLanguage"]

            if self.service == "noovo":
                episode_info_resp = self.tool.episode_id_url(episode["axisId"])
                service_hub_name = episode_info_resp["data"]["axisContent"]["authConstraints"][0]["packageName"]

                if episode_info_resp["data"]["axisContent"]["playbackMetadata"][0]["indicator"] != "DESCRIBED_VIDEO":
                    options["audio_description"] = False

                if len(episode_info_resp["data"]["axisContent"]["playbackMetadata"][1]["languages"]) >= 2:
                    options["language"] = "FR"
                else:
                    options["language"] = episode_info_resp["data"]["axisContent"]["playbackMetadata"][1]["languages"][0]["languageCode"]

                if len(episode_info_resp["data"]["axisContent"]["playbackMetadata"]) >= 3:
                    if episode_info_resp["data"]["axisContent"]["playbackMetadata"][2]["indicator"] != "CLOSED_CAPTIONS":
                        options["subs"] = False
            
    
            if episode["seasonNumber"] == 0 and episode["episodeNumber"] == 0:
                options["clean_name"] = chosen_episodes["title"]
                options["path"] = tools.clean_filename(f'{chosen_episodes["title"]}.{chosen_episodes["releaseYear"]}.{options["language"].upper()}')
            
            else:
                options["path"] = f'{tools.clean_filename(chosen_episodes["title"])}.S{episode["seasonNumber"]:02}E{episode["episodeNumber"]:02}.{options["language"].upper()[:2]}'
                options["clean_name"] = f'{chosen_episodes["title"]} Saison {episode["seasonNumber"]} Episode {episode["episodeNumber"]}'
    
            if options["audio_description"]:
                options["path"] += ".AD"
            
            options["path"] += f'.{options["resolution"]}p{custom_string}'
    
            self.download_content(episode["axisId"], episode["destinationCode"],  options)
    
    
    def download_content(self, id: int, service_hub_name: str, options):
    
        config_resp = self.tool.service_config(self.service)
    
        episode_second_id_resp = self.tool.second_episode_id(id, service_hub_name)
        
        if len(episode_second_id_resp["Items"]) == 0:
            print("You need an account to access this content")
            exit()
        
        second_id = episode_second_id_resp["Items"][0]["Id"]
    
        low_res_mpd = self.tool.mpd_url(id, second_id, service_hub_name, options["headers"])
    
        options["mpd_url"] = low_res_mpd.replace("best", "ultimate")
        options["subs_url"] = self.tool.subtitles_url(id, second_id, service_hub_name)
    
        options["licence_url"] = config_resp["api"]["drmLicenceServerUrl"] + "/widevine"

        if self.service == "crave":
            clean_auth_token = options["headers"]["Authorization"].replace("Bearer ", "")

            options["licence_url"] += "?jwt=" + clean_auth_token
            options["subs_url"] += "?jwt=" + clean_auth_token
    

        return self.download_bell(options)
    
    def download_bell(self, options):

        options["pssh"] = dash.get_pssh(options["mpd_url"], options["quiet"])
    
        options["decryption_keys"] = dash.setup_licence_challenge(options["pssh"], options["licence_url"], options["wvd_path"], options["headers"])

        if options["subs"]:
            vtt_text = requests.get(options["subs_url"], headers=options["headers"]).content
            if self.service == "crave":
                vtt_text = requests.get(vtt_text, headers=options["headers"]).content
            
            with open(f"{options['path']}.vtt", "wb") as f:
                f.write(vtt_text)

        tools.n_m3u8dl_re_download(options)
        tools.remove_phantom_subs(options)
        tools.mkvmerge_merge(options)



    
    def help(self):
        print(self.tool.help_text)
        exit()
    
    def connect(self):
        return bell_tokens.login(self.settings_path, self.service)
    
    def search(self, args):
        if len(args) > 3:
            return self.search_shows(args[3])
        else:
            return self.search_shows("")
    
    
    def list(self, args):
        if len(args) > 3:
            if not self.tool.validate_url(args[3]):
                shows = self.search_shows(args[3])
                if len(shows) == 0:
                    print(f"No result for search {args[3]}")
                    exit()
                return self.list_episodes(shows[0])
    
    def info(self, args):
        if len(args) > 3:
            if not self.tool.validate_url(args[3]):
                shows = self.search_shows(args[3])
                if len(shows) == 0:
                    print(f"No result for search {args[3]}")
                    exit()
                return self.show_info(shows[0])
        
    
    def download(self, args):
    
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
            
            shows = ""

            if len(args) > 3:
                if not self.tool.validate_url(args[3]):
                    shows = self.search_shows(args[3])
                    if len(shows) == 0:
                        print(f"No result for search {args[3]}")
                        exit()
            
            seasons_episodes = ""
            if len(args) > 4:
                if args[4][1:] != "-":
                    seasons_episodes = args[4]
    
            
            options = {
                "resolution": resolution,
                "quiet": quiet,
                "audio_description": audiodescription,
                "allow_trailers": allow_trailers,
                "subs": subs
            }
            
            self.get_download(shows[0], latest, seasons_episodes, options)



            

args = sys.argv
bell_media = Bell_Media()

if len(args) < 3:
    #print(crave_tools.help_text)
    #bell_media.tool = noovo_tools
    #bell_media.service = "noovo"
    #args.append(bell_media.service)
    #args.append("download")
    #args.append("occupation double mexique")
    #args.append("s8e79-s8e79")
    #args.append("-r")
    #args.append("1080")
    #args.append("-s")
    #args.append("-ad")
    #args.append("download")
    #args.append("med")
    #args.append("-l")
    #args.append("download")
    #args.append("")
    #args.append("-l")
    #args.append("-q")
    #args.append("-r")
    #args.append("360")

    #bell_media.download(args)

    exit()

else:
    bell_media.service = args[1]

if bell_media.service == "crave":
    bell_media.tool = crave_tools

if bell_media.service == "noovo":
    bell_media.tool = noovo_tools


if args[2] == "help":
    bell_media.help()



if args[2] == "connect":
    bell_media.connect()


if args[2] == "search":
    bell_media.search(args)



if args[2] == "list":
    bell_media.list(args)
    


if args[2] == "info":
    bell_media.info(args)

if args[2] == "download":
    bell_media.download(args)