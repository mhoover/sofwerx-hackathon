# SOFWERX Hackathon
## Introduction
[SOFWERX](www.sofwerx.org) is an organization dedicated to helping develop advanced solutions for U.S. Special Forces by bringing different thought to hard problems. From 12-13 May 2017, SOFWERX hosted a [hackathon](http://www.sofwerx.org/openwerx-hackathon/) to help further their mission.

## Challenges
### [Bounty Hunter](http://www.hackathon.io/openwerx-hackathon)

- Somewhere off the coast of South Korea is a ship with hostages. You will have to predict where the ship is located based on the analysis of incomplete data (AIS, satellite imagery). But be careful - the weather might throw off your predictions or block the view of the satellite!
- You will be provided with:
    - An incomplete set of AIS data of the target ship
    - Location of APIs for environmental data information (wind, currents, cloud cover)
    - Location of APIs to request satellite imagery
    - Location of APIs to derive satellite orbital data
- (Check the [Rules](http://www.hackathon.io/openwerx-hackathon/rules) for a comprehensive set of links to the data and other resources provided for this challenge.)
- You must:
    - Use the AIS and environmental data to predict the ship route from the last known AIS position.
    - Use the orbital data to predict when the satellite might have imaged the ship so you know how to query the satellite imagery API for likely candidates.
    - Obtain likely imagery of the ship.
    - Finally, you will have to use the likely imagery to perform visual identification and determine the last known location of the ship!. Extra credit if you can derive the approximate speed!
- This challenge is sponsored by USSOCOM J24-Systems, and will be judged by John Hauenstein, Chief Systems Engineer, as well as [Jared Lander](https://www.landeranalytics.com/).

### [Master Maven](http://www.hackathon.io/openwerx-data)

- SOCOM is building an advanced, armored exoskeleton. Can you find out who is the worldwide leading expert in applying novel materials to personnel armor? Be prepared to argue your approach, your data, and ultimately your analysis.
- Check the [Rules](http://www.hackathon.io/openwerx-data/rules) for a set of links to potential data sources and other resources provided for this challenge.
- You must:
    - Perform selective searching, scrape/crawl, ingest, and structured (text)/unstructured (link) processing.
    - Use analytical techniques such as Social Network Analysis (SNA), sentiment, and other textual approaches that provide insight into content, relationships, context, and meaning.
    - Identify the most expert person in personnel armor material science based on their education, experience, institutional affiliation, and other signals of social and professional esteem.
- This challenge is sponsored by SOCOM Agile Acquisition, and will be judged by Joe Fritz, SOFWERX Program Manager.

### [Grey Pill](http://www.hackathon.io/openwerx-data1)

- New communities are growing on the internet, but they are using decentralized architectures, peer-to-peer protocols, and cultural codes (emojis, meme gifs, etc) that make it harder to survey, map, and understand. Your challenge is to explore this new ecosystem and develop novel data science techniques to illuminate it.
- You will be provided with a list of platform and protocol sources (Check the [Rules](http://www.hackathon.io/openwerx-data1/rules) for a comprehensive set of links to the data and other resources provided for this challenge.)
- You must:
    - Scrape and ingest a representative set of content from each resource provided.
    - Perform text analysis (including entity extraction/identification, sentiment, etc) on all unstructured and structured text fields. This includes translating from the source language to English (at some point in the overall analytical pipeline)
    - Perform graph/SNA-type analysis on all relationship data (post, author, comment, etc)
    - Perform analysis on all media posted. Goal is to derive as much context as possible from a given media post as well as context of the collective post (media, non-media such as tags, comments, etc), and any other topical/contextual "channels".
    - Finally, you will have to provide an overall "contextual dashboard" to illustrate the topical/semantic/sentimental trends within and across different platforms and protocols. Extra credit for a "Grey Network Weather Report" that can illustrate probabilistic correlation over time series across all sources ingested.
- This challenge is sponsored by Donovan Group, SOCOM J-5, and will be judged by Maj Jen Snow.

## Judging Criteria

- Conceptual approach to the problem
- The work done to solve/answer the problem
- How solution is presented

## Team

- Name: Team SMURF (Social Measurements Utilizing Random Federates)
- Members:
    - [Matt Hoover](matthew.a.hoover@gmail.com)
- Project: Grey Pill


START WITH WHY!!!
Then the what and how
Upload to YouTube by 5pm (public), then send link
    - emphasize probabilistic nature
    -
