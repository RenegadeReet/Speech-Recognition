import time

import requests
from API_Code import API_ASSEMBLY_AI


#UPLOAD

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_ASSEMBLY_AI}

filename = 'Output.wav'

def upload(filename):

    def read_file( filename , chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': API_ASSEMBLY_AI}
    response = requests.post(upload_endpoint,
                            headers = headers,
                            data = read_file(filename))


    audio_url = response.json()['upload_url']
    return audio_url

#TRANSCRIPTION

def transcription(audio_url):

    json = {"audio_url": audio_url}

    response = requests.post(transcription_endpoint , json=json, headers=headers)

    transcript_id = response.json()['id']
    return transcript_id

#POLLING

def poll(transcript_id):

    polling_endpoint = transcription_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint , headers=headers)

    return polling_response.json()

def transcription_result( audio_url ):

    transcript_id = transcription(audio_url)
    while True:
        poll_response = poll(transcript_id)
        if poll_response['status'] == 'completed':
            return poll_response
        elif poll_response['status'] == 'error':
            return poll_response['error']

        print("Waiting for 30 secs....")
        time.sleep((30))


def save_transcript(audio_url):
    data = transcription_result(audio_url)
    text_file=filename+".txt"

    if data:
        with open(text_file,"w") as f:
            f.write(data['text'])
    else:
        print("Error")

audio_url = upload(filename)
save_transcript(audio_url)


