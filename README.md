# Google Speech Recognition
Implementation of retreiving sound from a microphone and fetching the Speech To Text using Google Clouds API.
The ```Python``` implementation allows for "unlimited" length of recordings but the recommended length is still < 1 minute per recording.

Each named folder contains different code implementations (such as C# and Python).

Note that each implementation require an API - key from Google. This is expected to be in \_key/GAPI.json and if it is not it should be defined on construction of object. 

## C#
* [x] Add Asynconous recognition.
* [ ] Add recognition outside of forms.

## Python
* [x] Add Asynchronous recognition for larger files.
* [x] Add support for streaming recognition.
  - * [x] Make recognition async.

## Warnings
Should be noted that the latest version is NOT tested as it is from another project. 
```main.py``` presents a somewhat outdated implementation example. 
