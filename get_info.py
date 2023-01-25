import requests
from pydictionary import Dictionary as Dict
from bing_image_downloader import downloader as image_downloader
import os
import openai

# read config.json and get api keys
import json
with open("config.json") as f:
    config = json.load(f)
    openai.api_key = config["GPT_API_KEY"]

def get_info(word):
    # word = Dict(word)
    # data = {
    #     "word" : word.word,
    #     "definition" : word.meanings()[0],
    #     "synonyms" : word.synonyms()
    # }
    
    # get data from openai
    definitionQuery = f"AP Human definition of '{word}' 1-2 sentence answer: "
    charactaristicsQuery = f"AP Human characteristic of '{word}' (1-3 words answer): "
    exampleQuery = f"a single AP Human example of '{word}' 1-5 word answer: "

    print("Query defintion")
    definition = openai.Completion.create(
        engine="text-davinci-003",
        prompt=definitionQuery,
        temperature=1,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0

    )
    print("Query charactaristics")
    charactaristics = openai.Completion.create(
        engine="text-davinci-003",
        prompt=charactaristicsQuery,
        max_tokens=256,
        top_p=1.0,
        temperature=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print("Query example")
    example = openai.Completion.create(
        engine="text-davinci-003",
        prompt=exampleQuery,
        temperature=1,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    data = {
        "word" : word,
        "definition" : definition.choices[0].text.strip(),
        "charactaristics": charactaristics.choices[0].text.strip(),
        "example": example.choices[0].text.strip()
    }

    example = data["example"].strip()
    try:
        image_downloader.download(example, limit=1, output_dir='images', adult_filter_off=True, force_replace=False, timeout=60, verbose=False)
        fn = os.listdir(f"images/{example}")[0]
        data["image_url"] = f'images/{example}/{fn}'
    except Exception as e:
        print(e)
        data["image_url"] = "images/404.jpg"
    return data


# print(get_info("apple"))