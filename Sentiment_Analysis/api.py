import time
import json
import requests
from API_Code import API_ASSEMBLY_AI


#UPLOAD

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_ASSEMBLY_AI}

#TRANSCRIPTION

def transcription(audio_url , sentiment_analysis):

    json = {'audio_url': audio_url ,
            'sentiment_analysis': sentiment_analysis }

    response = requests.post(transcription_endpoint , json=json, headers=headers)

    transcript_id = response.json()['id']
    return transcript_id

#POLLING

def poll(transcript_id):

    polling_endpoint = transcription_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint , headers=headers)

    return polling_response.json()

def transcription_result( audio_url , sentiment_analysis):

    transcript_id = transcription(audio_url , sentiment_analysis)
    while True:
        poll_response = poll(transcript_id)
        if poll_response['status'] == 'completed':
            return poll_response
        elif poll_response['status'] == 'error':
            return poll_response['error']

        print("Waiting for 15 secs....")
        time.sleep(15)


def save_transcript(audio_url , filename , sentiment_analysis=False):

    data = transcription_result(audio_url , sentiment_analysis )
    text_file = filename+".txt"

    if data:
        with open(text_file , "w") as f:
            f.write(data["text"])
        if sentiment_analysis:
            sentiment_file = filename+"_sentiments.txt"
            with open(sentiment_file, "w") as f:
                json.dump(data["sentiment_analysis_results"], f, indent=4)
    else:
        print("Error")





