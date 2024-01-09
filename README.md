# json-manifest-to-mpd
A tool to convert Json Video Manifests into Dash ones (MPEG-DASH MPD)


#### Note
- initially made to convert Spotify Podcast manifests into MPD to stream using your own video player. i have not tested (or found) other services but i imagine it would be similar.

- it will convert Widevine DRM'd manifests but they cannot be streamed without the decryption keys.

## Usage
### Basic usage
With python or python3 installed
1. Clone the repository or download 'mpd.py'
2. Copy the json manifest into 'manifest.json'
3. `python3 mpd.py -i manifest.json -o output.mpd`
4. Your completed MPD will be 'output.mpd'

### General usage
1. Follow step 1 and 2 above
2. Read usage below
```
usage: mpd.py [-h] -i INPUT -o OUTPUT [-vo] [-ao] [-so] [--lowest] [--highest]
              [--avc_only] [--vp9_only] [--print_mpd]

Convert JSON video manifest to DASH MPD

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input JSON file
  -o OUTPUT, --output OUTPUT
                        Output MPD file
  -vo, --video_only     Only include video
  -ao, --audio_only     Only include audio
  -so, --sub_only       Only include subtitles
  --lowest              Only include lowest bitrate
  --highest             Only include highest bitrate
  --avc_only            Only include AVC
  --vp9_only            Only include VP9
  --print_mpd           Print MPD to console
```

## To-do
- [x] Allow for input and output files to be specified with arguments
- [x] Allow for choosing video, audio or sub only
- [x] Allow for lowest bitrate only
- [x] Allow for highest bitrate only
- [x] Allow for avc or vp9 only
- [x] Allow print MPD only
- [ ] More?

## Disclaimer
I don't promote or condone the use of this for piracy.