import string
import requests



def validate_url(show_path: str):
    accepted_characters: str = string.ascii_lowercase + "-/"
    for char in show_path:
        if char not in accepted_characters:
            return False
    
    req_url, headers = show_path_url(show_path)
    
    resp = requests.get(req_url)

    if resp.status_code != 200:
        return False
        
    if "errors" in resp.text:
        resp = requests.get(req_url, headers=headers)
        if "errors" in resp.text:
            return False

    return True


def show_id_url(show_id: str, show_path: str):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "DNT": "1",
        "graphql-client-platform": "entpay_web",
        "Priority": "u=4",
        "Referer": f"https://noovo.ca{show_path}",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    encoded_show_id = show_id.replace("/", "%2F")

    url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=axisMedia&variables=%7B%22axisMediaId%22%3A%22{encoded_show_id}%22%2C%22subscriptions%22%3A%5B%22CANAL_D%22%2C%22CANAL_VIE%22%2C%22INVESTIGATION%22%2C%22NOOVO%22%2C%22Z%22%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22UNAUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22f0ba1b6eb93a1ce5b545f67867a4e1f394d1c19744b2b381555e6c2137126e60%22%7D%7D"

    return url, headers

def show_path_url(show_path: str):

    #headers = {
    #    "graphql-client-platform": "entpay_web",
    #    "Sec-Fetch-Mode": "cors",
    #    "Sec-Fetch-Site": "same-origin"
    #}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "DNT": "1",
        "graphql-client-platform": "entpay_web",
        "Priority": "u=4",
        "Referer": f"https://noovo.ca{show_path}",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    encoded_show_path = show_path.replace("/", "%2F")

    url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=resolvePath&variables=%7B%22page%22%3A0%2C%22path%22%3A%22{encoded_show_path}%22%2C%22subscriptions%22%3A%5B%22CANAL_D%22%2C%22CANAL_VIE%22%2C%22INVESTIGATION%22%2C%22NOOVO%22%2C%22Z%22%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22UNAUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2226d314b59ba2708d261067964353f9a92f1c2689f50d1254fa4d03ddb9b9092a%22%7D%7D"
    #url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=resolvePath&variables=%7B%22page%22%3A0%2C%22path%22%3A%22{encoded_show_path}%22%2C%22subscriptions%22%3A%5B%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22AUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2226d314b59ba2708d261067964353f9a92f1c2689f50d1254fa4d03ddb9b9092a%22%7D%7D"

    return url, headers


def season_id_url(season_id: str, show_path: str):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "DNT": "1",
        "graphql-client-platform": "entpay_web",
        "Priority": "u=4",
        "Referer": f"https://noovo.ca{show_path}",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }


    body = {
        "operationName": "season",
        "variables": {
            "subscriptions": [
                "CANAL_D",
                "CANAL_VIE",
                "INVESTIGATION",
                "NOOVO",
                "Z"
            ],
            "maturity": "ADULT",
            "language": "FRENCH",
            "authenticationState": "UNAUTH",
            "playbackLanguage": "FRENCH",
            "seasonId": season_id
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "10abba25f3ccf874545f974851ff5fcd9d6734dff5207135e9faa5b9881567e7"
            }
        },
        "query": "query season($seasonId: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {\n  axisSeason(id: $seasonId) {\n    episodes {\n      previewMode\n      path\n      id\n      axisId\n      title\n      duration\n      seasonNumber\n      contentType\n      broadcastDate\n      axisPlaybackLanguages {\n        ...AxisPlaybackData\n        __typename\n      }\n      authConstraints {\n        ...AuthConstraintsData\n        __typename\n      }\n      playbackMetadata {\n        indicator\n        languages {\n          languageCode\n          languageDisplayName\n          __typename\n        }\n        __typename\n      }\n      thumbnailImages: images(formats: THUMBNAIL) {\n        url\n        __typename\n      }\n      badges {\n        label\n        title\n        __typename\n      }\n      episodeNumber\n      description\n      summary\n      __typename\n      badges {\n        title\n        label\n        __typename\n      }\n    }\n    __typename\n  }\n}\n\nfragment AuthConstraintsData on AuthConstraint {\n  authRequired\n  packageName\n  endDate\n  language\n  startDate\n  subscriptionName\n  __typename\n}\n\nfragment AxisPlaybackData on AxisPlayback {\n  destinationCode\n  language\n  duration\n  playbackIndicators\n  partOfMultiLanguagePlayback\n  __typename\n}\n"
    }


    encoded_season_id = season_id.replace("/", "%2F")

    url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=season&variables=%7B%22subscriptions%22%3A%5B%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22AUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%2C%22seasonId%22%3A%22{encoded_season_id}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2210abba25f3ccf874545f974851ff5fcd9d6734dff5207135e9faa5b9881567e7%22%7D%7D"
    url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=season&variables=%7B%22subscriptions%22%3A%5B%22CANAL_D%22%2C%22CANAL_VIE%22%2C%22INVESTIGATION%22%2C%22NOOVO%22%2C%22Z%22%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22UNAUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%2C%22seasonId%22%3A%22{encoded_season_id}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2210abba25f3ccf874545f974851ff5fcd9d6734dff5207135e9faa5b9881567e7%22%7D%7D"
    url = "https://www.noovo.ca/space-graphql/apq/graphql"

    return url, headers, body

def episode_id_url(episode_id: str):


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "DNT": "1",
        "graphql-client-platform": "entpay_web",
        "Priority": "u=4",
        #"Referer": f"https://noovo.ca{show_path}",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    body = {
        "operationName": "axisContent",
        "variables": {
            "id": episode_id,
            "subscriptions": [
                "CANAL_D",
                "CANAL_VIE",
                "INVESTIGATION",
                "NOOVO",
                "Z"
            ],
            "maturity": "ADULT",
            "language": "FRENCH",
            "authenticationState": "UNAUTH",
            "playbackLanguage": "FRENCH"
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "d6e75de9b5836cd6305c98c8d2411e336f59eb12f095a61f71d454f3fae2ecda"
            }
        },
        "query": "query axisContent($id: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {\n  axisContent(id: $id) {\n    axisId\n    id\n    path\n    title\n    duration\n    agvotCode\n    description\n    episodeNumber\n    seasonNumber\n    pathSegment\n    genres {\n      name\n      __typename\n    }\n    axisMedia {\n      heroBrandLogoId\n      id\n      title\n      __typename\n    }\n    adUnit {\n      ...AxisAdUnitData\n      __typename\n    }\n    authConstraints {\n      ...AuthConstraintsData\n      __typename\n    }\n    axisPlaybackLanguages {\n      ...AxisPlaybackData\n      __typename\n    }\n    originalSpokenLanguage\n    ogFields {\n      ogDescription\n      ogImages {\n        url\n        __typename\n      }\n      ogTitle\n      __typename\n    }\n    playbackMetadata {\n      indicator\n      languages {\n        languageCode\n        languageDisplayName\n        __typename\n      }\n      __typename\n    }\n    seoFields {\n      seoDescription\n      seoTitle\n      seoKeywords\n      canonicalUrl\n      __typename\n    }\n    badges {\n      title\n      label\n      __typename\n    }\n    posterImages: images(formats: POSTER) {\n      url\n      __typename\n    }\n    broadcastDate\n    expiresOn\n    startsOn\n    keywords\n    videoPageLayout {\n      __typename\n      ... on Rotator {\n        id\n        config {\n          ...RotatorConfigData\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n}\n\nfragment AxisAdUnitData on AxisAdUnit {\n  adultAudience\n  heroBrand\n  pageType\n  product\n  revShare\n  title\n  analyticsTitle\n  keyValue {\n    webformType\n    adTarget\n    contentType\n    mediaType\n    pageTitle\n    revShare\n    subType\n    __typename\n  }\n  __typename\n}\n\nfragment RotatorConfigData on RotatorConfig {\n  displayTitle\n  displayTotalItemCount\n  displayDots\n  style\n  imageFormat\n  lightbox\n  carousel\n  titleLinkMode\n  maxItems\n  disableBadges\n  customTitleLink {\n    ...LinkData\n    __typename\n  }\n  hideMediaTitle\n  __typename\n}\n\nfragment LinkData on Link {\n  buttonStyle\n  urlParameters\n  renderAs\n  linkType\n  linkLabel\n  longLinkLabel\n  linkTarget\n  userMgmtLinkType\n  url\n  id\n  showLinkLabel\n  internalContent {\n    title\n    __typename\n    ... on AxisContent {\n      axisId\n      authConstraints {\n        ...AuthConstraintsData\n        __typename\n      }\n      agvotCode\n      __typename\n    }\n    ... on AceWebContent {\n      path\n      pathSegment\n      __typename\n    }\n    ... on Section {\n      containerType\n      path\n      __typename\n    }\n    ... on AxisObject {\n      axisId\n      title\n      __typename\n    }\n    ... on TabItem {\n      sectionPath\n      __typename\n    }\n  }\n  hoverImage {\n    title\n    imageType\n    url\n    __typename\n  }\n  image {\n    id\n    width\n    height\n    title\n    url\n    altText\n    __typename\n  }\n  bannerImages {\n    breakPoint\n    image {\n      id\n      title\n      url\n      altText\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AuthConstraintsData on AuthConstraint {\n  authRequired\n  packageName\n  endDate\n  language\n  startDate\n  subscriptionName\n  __typename\n}\n\nfragment AxisPlaybackData on AxisPlayback {\n  destinationCode\n  language\n  duration\n  playbackIndicators\n  partOfMultiLanguagePlayback\n  __typename\n}\n"
    }


    #encoded_episode_id = episode_id.replace("/", "%2F")

    #url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=axisContent&variables=%7B%22id%22%3A%22{encoded_episode_id}%22%2C%22subscriptions%22%3A%5B%22CANAL_D%22%2C%22CANAL_VIE%22%2C%22INVESTIGATION%22%2C%22NOOVO%22%2C%22Z%22%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22UNAUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22d6e75de9b5836cd6305c98c8d2411e336f59eb12f095a61f71d454f3fae2ecda%22%7D%7D"
    url = "https://www.noovo.ca/space-graphql/apq/graphql"

    return url, headers, body



def search_body(query: str):
    url = "https://www.noovo.ca/space-graphql/apq/graphql"
    
    body = {
      "operationName": "searchResults",
      "variables": {
        "page": 0,
        "title": query,
        "pageSize": 100,
        "subscriptions": [
          "CANAL_D",
          "CANAL_VIE",
          "INVESTIGATION",
          "NOOVO",
          "Z"
        ],
        "maturity": "ADULT",
        "language": "FRENCH",
        "authenticationState": "AUTH",
        "playbackLanguage": "FRENCH"
      },
      "extensions": {
        "persistedQuery": {
          "version": 1,
          "sha256Hash": "103c235ca0dd00919a66af6c1a85bf76de330fc38c98ae2410ff8173d5a614d8"
        }
      },
      "query": "query searchResults($title: String!, $pageSize: Int!, $page: Int = 0, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {\n  searchResults: searchMedia(titleMatches: $title, pageSize: $pageSize) {\n    ... on Medias {\n      page(page: $page) {\n        totalItemCount\n        totalPageCount\n        hasNextPage\n        items {\n          id\n          title\n          summary\n          agvotCode\n          qfrCode\n          axisId\n          path\n          metadataUpgrade {\n            ...AxisMetaDataUpgradeData\n            __typename\n          }\n          posterImages: images(formats: POSTER) {\n            url\n            __typename\n          }\n          squareImages: images(formats: SQUARE) {\n            url\n            __typename\n          }\n          thumbnailImages: images(formats: THUMBNAIL) {\n            url\n            __typename\n          }\n          badges {\n            title\n            label\n            __typename\n          }\n          firstPlayableContent {\n            ...FirstPlayableContentData\n            __typename\n          }\n          genres {\n            name\n            __typename\n          }\n          firstAirYear\n          originatingNetworkLogoId\n          heroBrandLogoId\n          seasons {\n            id\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FirstPlayableContentData on AxisContent {\n  id\n  title\n  axisId\n  path\n  seasonNumber\n  episodeNumber\n  summary\n  duration\n  authConstraints {\n    ...AuthConstraintsData\n    __typename\n  }\n  axisPlaybackLanguages {\n    ...AxisPlaybackData\n    __typename\n  }\n  playbackMetadata {\n    indicator\n    languages {\n      languageCode\n      languageDisplayName\n      __typename\n    }\n    __typename\n  }\n  featureImages: images(formats: THUMBNAIL) {\n    url\n    __typename\n  }\n  badges {\n    title\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment AuthConstraintsData on AuthConstraint {\n  authRequired\n  packageName\n  endDate\n  language\n  startDate\n  subscriptionName\n  __typename\n}\n\nfragment AxisPlaybackData on AxisPlayback {\n  destinationCode\n  language\n  duration\n  playbackIndicators\n  partOfMultiLanguagePlayback\n  __typename\n}\n\nfragment AxisMetaDataUpgradeData on AxisMetadataUpgrade {\n  displayPackageName\n  languages\n  packageName\n  subText\n  upgradeIconType\n  upgradeVisibility {\n    descriptiveReason\n    displayLabel\n    upgradeVisible\n    __typename\n  }\n  userIsSubscribed\n  __typename\n}\n"
    }

    return url, body
