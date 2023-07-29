# json-manifest-to-mpd
A tool to convert Json Video Manifests into Dash ones (MPEG-DASH MPD)


#### Note
- initially made to convert Spotify Podcast manifests into MPD to stream using your own video player. i have not tested (or found) other services but i imagine it would be similar.

- it will convert Widevine DRM'd manifests but they cannot be streamed without the decryption keys.

## Usage
With python or python3 installed
1. Clone the repository or download 'mpd.py'
2. Copy the json manifest into 'manifest.json'
3. `python3 mpd.py`
4. Your completed MPD will be 'output.mpd'

## To-do
- Allow for input and output files to be specified with arguments
- Allow for choosing video, audio or sub only
- Allow for lowest bitrate only
- Allow for highest bitrate only
- Allow for avc or vp9 only
- Allow print MPD only

## Disclaimer
I don't promote or condone the use of this for piracy.