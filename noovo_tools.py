import string
import requests
import urllib.parse
import json

def validate_url(show_path: str):
    accepted_characters: str = string.ascii_lowercase + string.digits + "-/"
    for char in show_path:
        if char not in accepted_characters:
            return False
    
    r = show_path_url(show_path)

    if r.status_code != 200 or "errors" in r.text:
        return False

    return True


def mpd_url(first_id: str, second_id: str, service_hub_name: str, headers):
    url = f"https://capi.9c9media.com/destinations/{service_hub_name}/platforms/desktop/playback/contents/{first_id}/contentPackages/{second_id}/manifest.mpd?action=reference&ssl=true&filter=fe&uhd=true&hd=true&mcv=false&mca=true&mta=true&tpt=false&stt=false"

    resp = "Error"

    while "Error" in resp:
        resp = requests.get(url, headers=headers).text
        
        if '"ErrorCode":"401"' in resp:
            print("You don't have access to this content")
            exit()

    return resp


def subtitles_url(first_id: str, second_id: str, service_hub_name: str):
    url = f"https://capi.9c9media.com/destinations/{service_hub_name}/platforms/desktop/playback/contents/{first_id}/contentPackages/{second_id}/manifest.vtt"

    return url


def second_episode_id(first_id: str, service_hub_name: str):
    url = f"https://capi.9c9media.com/destinations/{service_hub_name}/platforms/desktop/contents/{first_id}/contentPackages?%24lang=fr"
    resp = {"errors": {}}
    
    while "errors" in resp.keys():
        resp = requests.get(url).json()
    
    return resp


def service_config(service_name: str):
    url = f"https://config.jasperplayer.com/v20231031/{service_name}/production/web/config.json"
    
    resp = {"errors": {}}
    
    while "errors" in resp.keys():
        resp = requests.get(url).json()
    
    return resp


def show_id_url(show_id: str):

    encoded_show_id: str = urllib.parse.quote_plus(show_id)

    url = f"https://www.noovo.ca/space-graphql/apq/graphql?operationName=axisMedia&variables=%7B%22axisMediaId%22%3A%22{encoded_show_id}%22%2C%22subscriptions%22%3A%5B%22CANAL_D%22%2C%22CANAL_VIE%22%2C%22INVESTIGATION%22%2C%22NOOVO%22%2C%22Z%22%5D%2C%22maturity%22%3A%22ADULT%22%2C%22language%22%3A%22FRENCH%22%2C%22authenticationState%22%3A%22UNAUTH%22%2C%22playbackLanguage%22%3A%22FRENCH%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22f0ba1b6eb93a1ce5b545f67867a4e1f394d1c19744b2b381555e6c2137126e60%22%7D%7D"

    resp = {"errors": {}}
    
    while "errors" in resp.keys():
        resp = requests.get(url).json()
    
    return resp

def show_path_url(show_path: str):

    body = {
        "operationName": "resolvePath",
        "variables": {
            "page": 0,
            "path": show_path,
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
                "sha256Hash": "26d314b59ba2708d261067964353f9a92f1c2689f50d1254fa4d03ddb9b9092a"
            }
        },
        "query": "query resolvePath($path: String!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $page: Int = 0) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {\n  resolvedPath(path: $path) {\n    redirected\n    path\n    segments {\n      position\n      content {\n        title\n        id\n        path\n        __typename\n      }\n      __typename\n    }\n    lastSegment {\n      position\n      content {\n        id\n        title\n        path\n        __typename\n        ... on AceWebContent {\n          path\n          ... on Rotator {\n            adUnit {\n              ...AceAdUnitData\n              __typename\n            }\n            __typename\n          }\n          ... on Article {\n            seoFields {\n              seoDescription\n              seoTitle\n              canonicalUrl\n              __typename\n            }\n            ogFields {\n              ...OGFields\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        ... on AxisObject {\n          __typename\n          description\n          axisId\n          ... on AxisContent {\n            keywords\n            adUnit {\n              ...AxisAdUnitData\n              __typename\n            }\n            seasonNumber\n            episodeNumber\n            contentType\n            seoFields {\n              ...SEOFields\n              __typename\n            }\n            ogFields {\n              ...OGFields\n              __typename\n            }\n            __typename\n          }\n          ... on AxisCollection {\n            adUnit {\n              ...AxisAdUnitData\n              __typename\n            }\n            seoFields {\n              ...SEOFields\n              __typename\n            }\n            __typename\n          }\n          ... on AxisMedia {\n            keywords\n            adUnit {\n              ...AxisAdUnitData\n              __typename\n            }\n            firstPlayableContent {\n              id\n              axisId\n              authConstraints {\n                ...AuthConstraintsData\n                __typename\n              }\n              axisPlaybackLanguages {\n                ...AxisPlaybackData\n                __typename\n              }\n              badges {\n                title\n                label\n                __typename\n              }\n              __typename\n            }\n            seoFields {\n              ...SEOFields\n              __typename\n            }\n            ogFields {\n              ...OGFields\n              __typename\n            }\n            __typename\n          }\n        }\n        ... on Section {\n          containerType\n          adUnit {\n            ...AceAdUnitData\n            __typename\n          }\n          gridConfig {\n            ...GridConfigData\n            __typename\n          }\n          secondNavigation {\n            title\n            renderTitleAs\n            titleImage {\n              __typename\n              id\n              url\n            }\n            links {\n              ...LinkData\n              __typename\n            }\n            __typename\n          }\n          firstPageLayout {\n            ...FirstPageLayoutData\n            __typename\n          }\n          seoFields {\n            ...SEOFields\n            __typename\n          }\n          ogFields {\n            ...OGFields\n            __typename\n          }\n          __typename\n        }\n        ... on Site {\n          adUnit {\n            ...AceAdUnitData\n            __typename\n          }\n          firstPageLayout {\n            ...FirstPageLayoutData\n            __typename\n          }\n          siteConfig {\n            ...SiteConfig\n            __typename\n          }\n          seoFields {\n            ...SEOFields\n            __typename\n          }\n          ogFields {\n            ...OGFields\n            __typename\n          }\n          __typename\n        }\n      }\n      __typename\n    }\n    searchResults {\n      ... on Medias {\n        page(page: $page) {\n          totalItemCount\n          totalPageCount\n          hasNextPage\n          items {\n            id\n            title\n            summary\n            agvotCode\n            qfrCode\n            axisId\n            path\n            metadataUpgrade {\n              ...AxisMetaDataUpgradeData\n              __typename\n            }\n            posterImages: images(formats: POSTER) {\n              url\n              __typename\n            }\n            squareImages: images(formats: SQUARE) {\n              url\n              __typename\n            }\n            thumbnailImages: images(formats: THUMBNAIL) {\n              url\n              __typename\n            }\n            firstPlayableContent {\n              ...FirstPlayableContentData\n              __typename\n            }\n            badges {\n              title\n              label\n              __typename\n            }\n            genres {\n              name\n              __typename\n            }\n            firstAirYear\n            originatingNetworkLogoId\n            heroBrandLogoId\n            seasons {\n              id\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Articles {\n        page(page: $page) {\n          totalItemCount\n          totalPageCount\n          hasNextPage\n          items {\n            id\n            title\n            path\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment GridConfigData on GridConfig {\n  sortingEnabled\n  availableSortingOptions\n  filterEnabled\n  displayTitle\n  displayTotalItemCount\n  numberOfColumns\n  style\n  imageFormat\n  lightbox\n  paging {\n    pageSize\n    pagingType\n    __typename\n  }\n  hideMediaTitle\n  __typename\n}\n\nfragment SEOFields on SEOFieldsWithKeywords {\n  seoDescription\n  seoTitle\n  seoKeywords\n  canonicalUrl\n  __typename\n}\n\nfragment AceAdUnitData on AceAdUnit {\n  adultAudience\n  heroBrand\n  pageType\n  product\n  revShare\n  title\n  analyticsTitle\n  keyValue {\n    webformType\n    adTarget\n    contentType\n    mediaType\n    pageTitle\n    revShare\n    subType\n    __typename\n  }\n  __typename\n}\n\nfragment AxisAdUnitData on AxisAdUnit {\n  adultAudience\n  heroBrand\n  pageType\n  product\n  revShare\n  title\n  analyticsTitle\n  keyValue {\n    webformType\n    adTarget\n    contentType\n    mediaType\n    pageTitle\n    revShare\n    subType\n    __typename\n  }\n  __typename\n}\n\nfragment SiteConfig on SiteConfig {\n  __typename\n  cravingsSection {\n    id\n    title\n    path\n    __typename\n  }\n  fallBackImageUrl {\n    url\n    title\n    __typename\n  }\n  searchConfig {\n    searchSection {\n      id\n      title\n      path\n      __typename\n    }\n    __typename\n  }\n  supportSection {\n    id\n    title\n    path\n    __typename\n  }\n  supportSearchResultsSection {\n    id\n    title\n    path\n    __typename\n  }\n  subscriptionFlowSection {\n    id\n    title\n    path\n    __typename\n  }\n  liveSection {\n    id\n    title\n    path\n    __typename\n  }\n  newsletterSection {\n    id\n    title\n    path\n    __typename\n  }\n  userPrompt {\n    __typename\n    ... on SurveyUserPrompt {\n      description\n      durationToComplete\n      interceptUrl\n      title\n      showInterval\n      actionButtonText\n      type\n      __typename\n    }\n    ... on Newsletter {\n      showInterval\n      newsletterTitle\n      newsletterDescription\n      newsletterLink {\n        ... on Link {\n          ...LinkData\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ... on InfoSplash {\n      type\n      modal {\n        title\n        id\n        ctaText\n        dismissButtonText\n        image {\n          altText\n          url\n          height\n          width\n          imageType\n          description\n          __typename\n        }\n        link {\n          ...LinkData\n          __typename\n        }\n        summary\n        interceptElapsedTime\n        __typename\n      }\n      __typename\n    }\n  }\n}\n\nfragment LinkData on Link {\n  buttonStyle\n  urlParameters\n  renderAs\n  linkType\n  linkLabel\n  longLinkLabel\n  linkTarget\n  userMgmtLinkType\n  url\n  id\n  showLinkLabel\n  internalContent {\n    title\n    __typename\n    ... on AxisContent {\n      axisId\n      authConstraints {\n        ...AuthConstraintsData\n        __typename\n      }\n      agvotCode\n      __typename\n    }\n    ... on AceWebContent {\n      path\n      pathSegment\n      __typename\n    }\n    ... on Section {\n      containerType\n      path\n      __typename\n    }\n    ... on AxisObject {\n      axisId\n      title\n      __typename\n    }\n    ... on TabItem {\n      sectionPath\n      __typename\n    }\n  }\n  hoverImage {\n    title\n    imageType\n    url\n    __typename\n  }\n  image {\n    id\n    width\n    height\n    title\n    url\n    altText\n    __typename\n  }\n  bannerImages {\n    breakPoint\n    image {\n      id\n      title\n      url\n      altText\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AuthConstraintsData on AuthConstraint {\n  authRequired\n  packageName\n  endDate\n  language\n  startDate\n  subscriptionName\n  __typename\n}\n\nfragment OGFields on OGFields {\n  ogDescription\n  ogImage {\n    url\n    __typename\n  }\n  ogAxisImage {\n    url\n    __typename\n  }\n  ogTitle\n  __typename\n}\n\nfragment FirstPageLayoutData on FirstPageLayout {\n  numberOfAds\n  pageSize\n  numberOfPages\n  totalRows\n  firstPageLayoutRows {\n    ...PageLayout\n    __typename\n  }\n  remainingPageLayoutRows {\n    ...PageLayoutSimplified\n    __typename\n  }\n  __typename\n}\n\nfragment PageLayout on PageLayoutRow {\n  row {\n    colwidth\n    elements {\n      __typename\n      id\n      ... on SearchResult {\n        placeholder\n        __typename\n      }\n      ... on Rotator {\n        path\n        title\n        hasPersonalizedCollection\n        config {\n          ...RotatorConfigData\n          __typename\n        }\n        AEMCollection {\n          ...AemCollectionData\n          __typename\n        }\n        hasPersonalizedCollection\n        collectionAttributes {\n          subType\n          options {\n            mediaTypes\n            keywords\n            genres\n            collectionId\n            __typename\n          }\n          __typename\n        }\n        collection {\n          page {\n            totalItemCount\n            __typename\n          }\n          __typename\n        }\n        videoStreams {\n          axisId\n          __typename\n        }\n        brandedRow\n        __typename\n      }\n      ... on Tab {\n        displayTitle\n        title\n        tabItems {\n          title\n          id\n          content {\n            __typename\n            id\n            ... on Grid {\n              hasPersonalizedCollection\n              collectionAttributes {\n                subType\n                __typename\n              }\n              __typename\n            }\n            ... on WatchHistoryElement {\n              title\n              id\n              paging {\n                pageSize\n                pagingType\n                __typename\n              }\n              hasPersonalizedCollection\n              collectionAttributes {\n                subType\n                __typename\n              }\n              __typename\n            }\n            ... on Link {\n              ...LinkData\n              __typename\n            }\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Grid {\n        title\n        hasPersonalizedCollection\n        config {\n          style\n          __typename\n        }\n        __typename\n      }\n      ... on Link {\n        ...LinkData\n        __typename\n      }\n      ... on AdElement {\n        adUnitType {\n          adType\n          height\n          id\n          title\n          width\n          __typename\n        }\n        __typename\n      }\n      ... on Sponsorship {\n        id\n        type\n        label\n        title\n        brandLinks {\n          ...LinkData\n          __typename\n        }\n        __typename\n      }\n      ... on SocialElement {\n        id\n        title\n        label\n        links {\n          ...LinkData\n          __typename\n        }\n        __typename\n      }\n      ... on Textarea {\n        text\n        title\n        id\n        __typename\n      }\n      ... on AceImage {\n        ...AceImageData\n        __typename\n      }\n      ... on IAPSubscriptionPackage {\n        basePackage\n        description\n        features {\n          featureTagLine\n          icon {\n            url\n            altText\n            __typename\n          }\n          id\n          title\n          __typename\n        }\n        logo {\n          altText\n          url\n          __typename\n        }\n        packagePriceTerm {\n          priceTerm\n          priceTermSuffix\n          __typename\n        }\n        name\n        price\n        priceTerm\n        promoted\n        promotedTagLine\n        resourceCode\n        title\n        __typename\n      }\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RotatorConfigData on RotatorConfig {\n  displayTitle\n  displayTotalItemCount\n  displayDots\n  style\n  imageFormat\n  lightbox\n  carousel\n  titleLinkMode\n  maxItems\n  disableBadges\n  customTitleLink {\n    ...LinkData\n    __typename\n  }\n  hideMediaTitle\n  __typename\n}\n\nfragment AemCollectionData on AEMCollection {\n  brand\n  categories\n  id\n  show\n  tags\n  title\n  type\n  __typename\n}\n\nfragment AceImageData on AceImage {\n  __typename\n  altText\n  description\n  height\n  imageType\n  width\n  imageURL: url\n  imageTitle: title\n}\n\nfragment PageLayoutSimplified on PageLayoutRow {\n  row {\n    colwidth\n    elements {\n      __typename\n      id\n      ... on SearchResult {\n        placeholder\n        __typename\n      }\n      ... on Rotator {\n        path\n        title\n        config {\n          ...RotatorConfigData\n          __typename\n        }\n        hasPersonalizedCollection\n        collectionAttributes {\n          subType\n          options {\n            mediaTypes\n            keywords\n            genres\n            collectionId\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Tab {\n        displayTitle\n        title\n        tabItems {\n          title\n          id\n          content {\n            __typename\n            id\n            ... on Grid {\n              hasPersonalizedCollection\n              collectionAttributes {\n                subType\n                __typename\n              }\n              __typename\n            }\n            ... on WatchHistoryElement {\n              title\n              id\n              paging {\n                pageSize\n                pagingType\n                __typename\n              }\n              hasPersonalizedCollection\n              collectionAttributes {\n                subType\n                __typename\n              }\n              __typename\n            }\n            ... on Link {\n              ...LinkData\n              __typename\n            }\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Grid {\n        title\n        hasPersonalizedCollection\n        config {\n          style\n          __typename\n        }\n        __typename\n      }\n      ... on Link {\n        ...LinkData\n        __typename\n      }\n      ... on AdElement {\n        adUnitType {\n          adType\n          height\n          id\n          title\n          width\n          __typename\n        }\n        __typename\n      }\n      ... on Sponsorship {\n        id\n        type\n        label\n        title\n        brandLinks {\n          ...LinkData\n          __typename\n        }\n        __typename\n      }\n      ... on SocialElement {\n        id\n        title\n        label\n        links {\n          ...LinkData\n          __typename\n        }\n        __typename\n      }\n      ... on Textarea {\n        text\n        title\n        id\n        __typename\n      }\n      ... on AceImage {\n        ...AceImageData\n        __typename\n      }\n      ... on IAPSubscriptionPackage {\n        basePackage\n        description\n        features {\n          featureTagLine\n          icon {\n            url\n            altText\n            __typename\n          }\n          id\n          title\n          __typename\n        }\n        logo {\n          altText\n          url\n          __typename\n        }\n        packagePriceTerm {\n          priceTerm\n          priceTermSuffix\n          __typename\n        }\n        name\n        price\n        priceTerm\n        promoted\n        promotedTagLine\n        resourceCode\n        title\n        __typename\n      }\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FirstPlayableContentData on AxisContent {\n  id\n  title\n  axisId\n  path\n  seasonNumber\n  episodeNumber\n  summary\n  duration\n  authConstraints {\n    ...AuthConstraintsData\n    __typename\n  }\n  axisPlaybackLanguages {\n    ...AxisPlaybackData\n    __typename\n  }\n  playbackMetadata {\n    indicator\n    languages {\n      languageCode\n      languageDisplayName\n      __typename\n    }\n    __typename\n  }\n  featureImages: images(formats: THUMBNAIL) {\n    url\n    __typename\n  }\n  badges {\n    title\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment AxisPlaybackData on AxisPlayback {\n  destinationCode\n  language\n  duration\n  playbackIndicators\n  partOfMultiLanguagePlayback\n  __typename\n}\n\nfragment AxisMetaDataUpgradeData on AxisMetadataUpgrade {\n  displayPackageName\n  languages\n  packageName\n  subText\n  upgradeIconType\n  upgradeVisibility {\n    descriptiveReason\n    displayLabel\n    upgradeVisible\n    __typename\n  }\n  userIsSubscribed\n  __typename\n}\n"
    }

    url = f"https://www.noovo.ca/space-graphql/apq/graphql"
    
    r = requests.post(url, data=json.dumps(body))

    return r


def season_id_url(season_id: str):


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

    url = "https://www.noovo.ca/space-graphql/apq/graphql"

    resp = {"errors": {}}
    
    while "errors" in resp.keys():
        resp = requests.post(url, data=json.dumps(body)).json()
    
    return resp

def episode_id_url(episode_id: str):

    body = {
        "operationName": "axisContent",
        "variables": {
            "id": f"contentid/axis-content-{episode_id}",
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

    url = "https://www.noovo.ca/space-graphql/apq/graphql"

    resp = {"errors": {}}
    
    while "errors" in resp.keys():
        resp = requests.post(url, data=json.dumps(body)).json()
    
    return resp



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

    resp = {"errors": {}}
    
    while "errors" in resp.keys():
        resp = requests.post(url, data=json.dumps(body)).json()
    
    return resp
