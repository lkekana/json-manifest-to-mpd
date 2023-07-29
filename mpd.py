from datetime import timedelta

def milliseconds_to_duration_str(duration_ms):
    duration_td = timedelta(milliseconds=duration_ms)
    duration_str = f"PT{duration_td.seconds}.{duration_td.microseconds:03d}S"
    return duration_str

import json

# Prompt the user for input and save it to a variable
# user_input = input("Enter JSON manifest: ")

# Read the JSON manifest from a file
with open('manifest.json') as f:
    user_input = f.read()

# Parse the JSON manifest into a Python dictionary
obj = json.loads(user_input)

# Find and convert duration of the video
duration = int(obj['contents'][0]['end_time_millis'])
duration_in_seconds = duration / 1000
duration_str = milliseconds_to_duration_str(duration)

MPD = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns="urn:mpeg:dash:schema:mpd:2011"
     xsi:schemaLocation="urn:mpeg:DASH:schema:MPD:2011 DASH-MPD.xsd"
     type="static"
     mediaPresentationDuration="''' + duration_str + '''"
     profiles="urn:mpeg:dash:profile:isoff-on-demand:2011">\n'''

segment_length_in_seconds = int(obj['contents'][0]['segment_length'])
segment_length_in_milliseconds = segment_length_in_seconds * 1000
timescale = segment_length_in_seconds * 1000

'''JSON manifest example:
{
    "contents": [
        {
            "segment_length": 4,
            "start_time_millis": 0,
            "end_time_millis": 12355040,
            "offline_profiles": [],
            "profiles": [
                {
                    "id": 18,
                    "audio_bitrate": 96000,
                    "audio_codec": "mp4a.40.2",
                    "mime_type": "audio/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 100806
                },
                {
                    "id": 17,
                    "video_bitrate": 200000,
                    "video_codec": "avc1.4d400d",
                    "video_resolution": 180,
                    "video_width": 320,
                    "video_height": 180,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 274004
                },
                {
                    "id": 16,
                    "video_bitrate": 400000,
                    "video_codec": "avc1.4d4015",
                    "video_resolution": 240,
                    "video_width": 426,
                    "video_height": 240,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 543050
                },
                {
                    "id": 15,
                    "video_bitrate": 600000,
                    "video_codec": "avc1.4d401e",
                    "video_resolution": 360,
                    "video_width": 640,
                    "video_height": 360,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 806906
                },
                {
                    "id": 14,
                    "video_bitrate": 800000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 480,
                    "video_width": 854,
                    "video_height": 480,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 1069008
                },
                {
                    "id": 13,
                    "video_bitrate": 1200000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 480,
                    "video_width": 854,
                    "video_height": 480,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 1595708
                },
                {
                    "id": 12,
                    "video_bitrate": 1600000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 720,
                    "video_width": 1280,
                    "video_height": 720,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 2117510
                },
                {
                    "id": 11,
                    "video_bitrate": 2000000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 720,
                    "video_width": 1280,
                    "video_height": 720,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 2663566
                },
                {
                    "id": 10,
                    "video_bitrate": 3000000,
                    "video_codec": "avc1.4d4028",
                    "video_resolution": 1080,
                    "video_width": 1920,
                    "video_height": 1080,
                    "mime_type": "video/mp4",
                    "file_type": "mp4",
                    "max_bitrate": 3936426
                },
                {
                    "id": 9,
                    "audio_bitrate": 96000,
                    "audio_codec": "mp4a.40.2",
                    "mime_type": "audio/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 148896
                },
                {
                    "id": 7,
                    "video_bitrate": 200000,
                    "video_codec": "avc1.4d400d",
                    "video_resolution": 180,
                    "video_width": 320,
                    "video_height": 180,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 308320
                },
                {
                    "id": 6,
                    "video_bitrate": 400000,
                    "video_codec": "avc1.4d4015",
                    "video_resolution": 240,
                    "video_width": 426,
                    "video_height": 240,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 583176
                },
                {
                    "id": 5,
                    "video_bitrate": 600000,
                    "video_codec": "avc1.4d401e",
                    "video_resolution": 360,
                    "video_width": 640,
                    "video_height": 360,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 849760
                },
                {
                    "id": 4,
                    "video_bitrate": 800000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 480,
                    "video_width": 854,
                    "video_height": 480,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 1120856
                },
                {
                    "id": 3,
                    "video_bitrate": 1200000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 480,
                    "video_width": 854,
                    "video_height": 480,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 1659664
                },
                {
                    "id": 2,
                    "video_bitrate": 1600000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 720,
                    "video_width": 1280,
                    "video_height": 720,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 2192080
                },
                {
                    "id": 1,
                    "video_bitrate": 2000000,
                    "video_codec": "avc1.4d401f",
                    "video_resolution": 720,
                    "video_width": 1280,
                    "video_height": 720,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 2747432
                },
                {
                    "id": 0,
                    "video_bitrate": 3000000,
                    "video_codec": "avc1.4d4028",
                    "video_resolution": 1080,
                    "video_width": 1920,
                    "video_height": 1080,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 4051400
                },
                {
                    "id": 23,
                    "audio_bitrate": 96000,
                    "audio_codec": "opus",
                    "mime_type": "audio/webm",
                    "file_type": "webm",
                    "max_bitrate": 113542
                },
                {
                    "id": 22,
                    "video_bitrate": 600000,
                    "video_codec": "vp9",
                    "video_resolution": 360,
                    "video_width": 640,
                    "video_height": 360,
                    "mime_type": "video/webm",
                    "file_type": "webm",
                    "max_bitrate": 833508
                },
                {
                    "id": 21,
                    "video_bitrate": 1200000,
                    "video_codec": "vp9",
                    "video_resolution": 480,
                    "video_width": 854,
                    "video_height": 480,
                    "mime_type": "video/webm",
                    "file_type": "webm",
                    "max_bitrate": 1432362
                },
                {
                    "id": 20,
                    "video_bitrate": 2000000,
                    "video_codec": "vp9",
                    "video_resolution": 720,
                    "video_width": 1280,
                    "video_height": 720,
                    "mime_type": "video/webm",
                    "file_type": "webm",
                    "max_bitrate": 2392406
                },
                {
                    "id": 19,
                    "video_bitrate": 3000000,
                    "video_codec": "vp9",
                    "video_resolution": 1080,
                    "video_width": 1920,
                    "video_height": 1080,
                    "mime_type": "video/webm",
                    "file_type": "webm",
                    "max_bitrate": 3474626
                }
            ],
            "background_profiles": [
                {
                    "id": 8,
                    "video_bitrate": 16000,
                    "video_codec": "avc1.4d400a",
                    "video_resolution": 4,
                    "video_width": 8,
                    "video_height": 4,
                    "mime_type": "video/mp2t",
                    "file_type": "ts",
                    "max_bitrate": 47376
                }
            ],
            "encryption_infos": []
        }
    ],
    "spritemaps": [
        {
            "id": 0,
            "height": 540,
            "width": 960,
            "number": 1
        }
    ],
    "start_time_millis": 0,
    "end_time_millis": 12355040,
    "initialization_template": "v1/origins/b1acc6dba4d449dcf7a71659d3fabea2/sources/dbdff182c8ea58b4aa22f93856acdc13/encodings/1576fb907a8d11ed81994be326b86994/profiles/{{profile_id}}/inits/{{file_type}}",
    "segment_template": "v1/origins/b1acc6dba4d449dcf7a71659d3fabea2/sources/dbdff182c8ea58b4aa22f93856acdc13/encodings/1576fb907a8d11ed81994be326b86994/profiles/{{profile_id}}/{{segment_timestamp}}.{{file_type}}",
    "subtitle_template": "v1/origins/b1acc6dba4d449dcf7a71659d3fabea2/sources/dbdff182c8ea58b4aa22f93856acdc13/{{language_code}}.webvtt",
    "spritemap_template": "v1/origins/b1acc6dba4d449dcf7a71659d3fabea2/sources/dbdff182c8ea58b4aa22f93856acdc13/encodings/1576fb907a8d11ed81994be326b86994/profiles/{{spritemap_id}}.jpg",
    "base_urls": [
        "https://video-akpcw-cdn-spotify-com.akamaized.net/segments/",
        "https://video-fa.scdn.co/segments/"
    ],
    "spritemap_base_urls": [
        "https://spritemaps.scdn.co/spritemaps/"
    ],
    "subtitle_base_urls": [
        "https://subtitles.spotifycdn.com/subtitles/"
    ],
    "subtitle_language_codes": [
        "en-US"
    ]
}
'''

#Using Json
# Add BaseURLS to the MPD
if (type(obj["base_urls"]) is list):
    for url in obj["base_urls"]:
        url = url.replace("&", "&amp;")
        MPD = MPD + "\t" + '<BaseURL>' + url + '</BaseURL>' + "\n"
else:
    MPD = MPD + "\t" + '<BaseURL>' + obj["base_urls"] + '</BaseURL>' + "\n"
    
# Create Period
MPD = MPD + "\t" + '<Period>' + "\n"

# Find AdaptationSets (Audio, Video, Subtitles)
# Video first
profiles = obj["contents"][0]["profiles"]
codecs = []
for profile in profiles:
    if profile["mime_type"] == "video/mp4" or profile["mime_type"] == "video/webm":
        arr = (profile["mime_type"], profile["video_codec"])  # Convert the list to a tuple
        codecs.append(arr)

unique_codecs = list(set(codecs))

for codec in unique_codecs:
    MPD = MPD + "\t\t" + '<AdaptationSet mimeType="' + codec[0] + '" codecs="' + codec[1] + '">' + "\n"
    for profile in profiles:
        # Proper method to include SegmentTimeline
        if (codec[0] == profile["mime_type"] and codec[1] == profile["video_codec"]):
            print("Adding video profile " + str(profile["id"]) + " to MPD")
            MPD = MPD + "\t\t\t" + '<Representation id="' + str(profile["id"]) + '" bandwidth="' + str(profile["max_bitrate"]) + '" width="' + str(profile["video_width"]) + '" height="' + str(profile["video_height"]) + '" frameRate="25">' + "\n"

            base = str(obj["segment_template"])
            base = base[:base.rfind("{{profile_id}}/") + 15] 
            base = base.replace("{{profile_id}}", str(profile["id"]))
            base = base.replace("&", "&amp;")
            MPD = MPD + "\t\t\t\t" + '<BaseURL>' + base + '</BaseURL>' + "\n"

            init = str(obj["initialization_template"])
            init = init[init.rfind("{{profile_id}}/") + 15:]
            init = init.replace("{{file_type}}", str(profile["file_type"])).replace("{{profile_id}}", str(profile["id"]))
            init = init.replace("&", "&amp;")
            # MPD = MPD + "\t\t\t\t" + '<Initialization sourceURL="' + init + '"/>' + "\n\n"


            media = str(obj["segment_template"])
            media = media[media.rfind("{{profile_id}}/") + 15:]
            media = media.replace("{{file_type}}", str(profile["file_type"]))
            media = media.replace("&", "&amp;")
            media = media.replace("{{segment_timestamp}}", "$Time$")
            # MPD = MPD + "\t\t\t\t" + '<SegmentTemplate timescale="1000" media="' + media + '">' + "\n"
            MPD = MPD + "\t\t\t\t" + '<SegmentTemplate media="' + media + '" initialization="' + init + '" duration="' + str(segment_length_in_milliseconds) + '" startNumber="0" timescale="' + str(timescale) + '">' + "\n"

            #Final Segment Timeline format
            '''
            <SegmentTimeline>
                <S t="0" d="4" r="3088"/>
            </SegmentTimeline>
            '''
            MPD = MPD + "\t\t\t\t\t" + '<SegmentTimeline>' + "\n"
            MPD = MPD + "\t\t\t\t\t\t" + '<S t="0" d="' + str(segment_length_in_seconds) + '" r="' + str(int(duration_in_seconds / segment_length_in_seconds)) + '"/>' + "\n"
            MPD = MPD + "\t\t\t\t\t" + '</SegmentTimeline>' + "\n"

            MPD = MPD + "\t\t\t\t" + '</SegmentTemplate>' + "\n"
            MPD = MPD + "\t\t\t" + '</Representation>' + "\n"

    MPD = MPD + "\t\t" + '</AdaptationSet>' + "\n\n"

# Audio next
profiles = obj["contents"][0]["profiles"]
codecs = []
for profile in profiles:
    if (profile["mime_type"] == "audio/mp4" or profile["mime_type"] == "audio/webm"):
        arr = (profile["mime_type"], profile["audio_codec"])  # Convert the list to a tuple
        codecs.append(arr)

unique_codecs = list(set(codecs))
for codec in unique_codecs:
    MPD = MPD + "\t\t" + '<AdaptationSet mimeType="' + codec[0] + '" codecs="' + codec[1] + '">' + "\n"
    for profile in profiles:
        if (codec[0] == profile["mime_type"] and codec[1] == profile["audio_codec"]):
            print("Adding audio profile " + str(profile["id"]) + " to MPD")
            MPD = MPD + "\t\t\t" + '<Representation id="' + str(profile["id"]) + '" bandwidth="' + str(profile["max_bitrate"]) + '">' + "\n"

            base = str(obj["segment_template"])
            base = base[:base.rfind("{{profile_id}}/") + 15]
            base = base.replace("{{profile_id}}", str(profile["id"]))
            base = base.replace("&", "&amp;")
            MPD = MPD + "\t\t\t\t" + '<BaseURL>' + base + '</BaseURL>' + "\n"

            init = str(obj["initialization_template"])
            init = init[init.rfind("{{profile_id}}/") + 15:]
            init = init.replace("{{file_type}}", str(profile["file_type"])).replace("{{profile_id}}", str(profile["id"]))
            init = init.replace("&", "&amp;")
            # MPD = MPD + "\t\t\t\t" + '<Initialization sourceURL="' + init + '"/>' + "\n\n"

            media = str(obj["segment_template"])
            media = media[media.rfind("{{profile_id}}/") + 15:]
            media = media.replace("{{file_type}}", str(profile["file_type"]))
            media = media.replace("&", "&amp;")
            media = media.replace("{{segment_timestamp}}", "$Time$")
            # MPD = MPD + "\t\t\t\t" + '<SegmentTemplate timescale="1000" media="' + media + '">' + "\n"
            MPD = MPD + "\t\t\t\t" + '<SegmentTemplate media="' + media + '" initialization="' + init + '" duration="' + str(segment_length_in_milliseconds) + '" startNumber="0" timescale="' + str(timescale) + '">' + "\n"

            #Final Segment Timeline format
            '''
            <SegmentTimeline>
                <S t="0" d="4" r="3088"/>
            </SegmentTimeline>
            '''
            MPD = MPD + "\t\t\t\t\t" + '<SegmentTimeline>' + "\n"
            MPD = MPD + "\t\t\t\t\t\t" + '<S t="0" d="' + str(segment_length_in_seconds) + '" r="' + str(int(duration_in_seconds / segment_length_in_seconds)) + '"/>' + "\n"
            MPD = MPD + "\t\t\t\t\t" + '</SegmentTimeline>' + "\n"


            MPD = MPD + "\t\t\t\t" + '</SegmentTemplate>' + "\n"
            MPD = MPD + "\t\t\t" + '</Representation>' + "\n"

    MPD = MPD + "\t\t" + '</AdaptationSet>' + "\n\n"

# Subtitle example
'''
<AdaptationSet mimeType="text/vtt" lang="en-US">
  <Representation id="subtitle_eng" mimeType="text/vtt" codecs="wvtt" bandwidth="0">
    <BaseURL>https://subtitles.spotifycdn.com/subtitles/v1/origins/b1acc6dba4d449dcf7a71659d3fabea2/sources/dbdff182c8ea58b4aa22f93856acdc13/en-US.webvtt</BaseURL>
  </Representation>
</AdaptationSet>
'''
# Subtitles last
sub_template = obj["subtitle_template"]
for sub in obj["subtitle_base_urls"]:
    for lang in obj["subtitle_language_codes"]:
        print("Adding subtitle " + str(lang) + " to MPD")
        MPD = MPD + "\t\t" + '<AdaptationSet mimeType="text/vtt" lang="' + str(lang) + '">' + "\n"
        MPD = MPD + "\t\t\t" + '<Representation id="subtitle_' + str(lang) + '" mimeType="text/vtt" codecs="wvtt" bandwidth="0">' + "\n"
        url = str(sub) + str(sub_template).replace("{{language_code}}",str(lang))
        url = url.replace("&", "&amp;")
        MPD = MPD + "\t\t\t\t" + '<BaseURL>' + url + '</BaseURL>' + "\n"
        MPD = MPD + "\t\t\t" + '</Representation>' + "\n"
        ## MPD = MPD + "\t\t\t" + url + "\n"
        MPD = MPD + "\t\t" + '</AdaptationSet>' + "\n"

# MPD end
MPD = MPD + "\t" + '</Period>' + "\n"
MPD = MPD + '</MPD>'

# Save MPD
f = open("output.mpd", "w")
f.write(MPD)
f.close()