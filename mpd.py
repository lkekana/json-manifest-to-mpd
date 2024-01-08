import json
from datetime import timedelta

def milliseconds_to_duration_str(duration_ms: int):
    duration_td = timedelta(milliseconds=duration_ms)
    duration_str = f"PT{duration_td.seconds}.{duration_td.microseconds:03d}S"
    return duration_str

def read_json_file(file_name: str):
    with open(file_name) as f:
        data = json.load(f)
    return data

def save_text_file(file_name: str, text: str):
    f = open(file_name, "w")
    f.write(text)
    f.close()

def make_mpd(obj: dict):
    # Find and convert duration of the video
    duration = int(obj['contents'][0]['end_time_millis'])
    duration_in_seconds = duration / 1000
    duration_str = milliseconds_to_duration_str(duration)

    # MPD declaration
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

    return MPD

def main():
    obj = read_json_file("manifest.json")
    MPD = make_mpd(obj)
    save_text_file("output.mpd", MPD)

if __name__ == "__main__":
    main()