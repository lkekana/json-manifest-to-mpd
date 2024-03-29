import json
from datetime import timedelta
import argparse
import os
import re

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

def make_video_adaptation_set(obj: dict, args: argparse.Namespace):
    MPD = ""
    
    duration = int(obj['contents'][0]['end_time_millis'])
    duration_in_seconds = duration / 1000
    segment_length_in_seconds = int(obj['contents'][0]['segment_length'])
    segment_length_in_milliseconds = segment_length_in_seconds * 1000
    timescale = segment_length_in_seconds * 1000

    profiles = obj["contents"][0]["profiles"]
    codecs = []
    for profile in profiles:
        if profile["mime_type"] == "video/mp4" or profile["mime_type"] == "video/webm":
            arr = (profile["mime_type"], profile["video_codec"], profile["max_bitrate"])
            codecs.append(arr)

    unique_codecs = list(set(codecs))

    if args.avc_only:
        codecs_copy = unique_codecs.copy()
        unique_codecs = []
        for codec in codecs_copy:
            if re.search(r'avc', codec[1]):
                unique_codecs.append(codec)
    elif args.vp9_only:
        codecs_copy = unique_codecs.copy()
        unique_codecs = []
        for codec in codecs_copy:
            if re.search(r'vp9', codec[1]):
                unique_codecs.append(codec)

    if args.lowest:
        unique_codecs.sort(key=lambda x: x[2])
        unique_codecs = [unique_codecs[0]]
    elif args.highest:
        unique_codecs.sort(key=lambda x: x[2], reverse=True)
        unique_codecs = [unique_codecs[0]]
    
    for codec in unique_codecs:
        added_something = False
        temp_MPD = "\t\t" + '<AdaptationSet mimeType="' + codec[0] + '" codecs="' + codec[1] + '">' + "\n"
        for profile in profiles:
            if (profiles[profiles.index(profile)].get("added") == True):
                continue

            # Proper method to include SegmentTimeline
            if (codec[0] == profile["mime_type"] and codec[1] == profile["video_codec"]):
                added_something = True
                print("Adding video profile " + str(profile["id"]) + " to MPD")
                temp_MPD = temp_MPD + "\t\t\t" + '<Representation id="' + str(profile["id"]) + '" bandwidth="' + str(profile["max_bitrate"]) + '" width="' + str(profile["video_width"]) + '" height="' + str(profile["video_height"]) + '" frameRate="25">' + "\n"

                base = str(obj["segment_template"])
                base = base[:base.rfind("{{profile_id}}/") + 15] 
                base = base.replace("{{profile_id}}", str(profile["id"]))
                base = base.replace("&", "&amp;")
                temp_MPD = temp_MPD + "\t\t\t\t" + '<BaseURL>' + base + '</BaseURL>' + "\n"

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
                temp_MPD = temp_MPD + "\t\t\t\t" + '<SegmentTemplate media="' + media + '" initialization="' + init + '" duration="' + str(segment_length_in_milliseconds) + '" startNumber="0" timescale="' + str(timescale) + '">' + "\n"

                #Final Segment Timeline format
                '''
                <SegmentTimeline>
                    <S t="0" d="4" r="3088"/>
                </SegmentTimeline>
                '''
                temp_MPD = temp_MPD + "\t\t\t\t\t" + '<SegmentTimeline>' + "\n"
                temp_MPD = temp_MPD + "\t\t\t\t\t\t" + '<S t="0" d="' + str(segment_length_in_seconds) + '" r="' + str(int(duration_in_seconds / segment_length_in_seconds)) + '"/>' + "\n"
                temp_MPD = temp_MPD + "\t\t\t\t\t" + '</SegmentTimeline>' + "\n"

                temp_MPD = temp_MPD + "\t\t\t\t" + '</SegmentTemplate>' + "\n"
                temp_MPD = temp_MPD + "\t\t\t" + '</Representation>' + "\n"

                profiles[profiles.index(profile)]["added"] = True

        if added_something:
            MPD = MPD + temp_MPD
            MPD = MPD + "\t\t" + '</AdaptationSet>' + "\n\n"
    
    return MPD

def make_audio_adaptation_set(obj: dict, args: argparse.Namespace):
    MPD = ""

    duration = int(obj['contents'][0]['end_time_millis'])
    duration_in_seconds = duration / 1000
    segment_length_in_seconds = int(obj['contents'][0]['segment_length'])
    segment_length_in_milliseconds = segment_length_in_seconds * 1000
    timescale = segment_length_in_seconds * 1000

    profiles = obj["contents"][0]["profiles"]
    codecs = []
    for profile in profiles:
        if (profile["mime_type"] == "audio/mp4" or profile["mime_type"] == "audio/webm"):
            arr = (profile["mime_type"], profile["audio_codec"], profile["max_bitrate"])
            codecs.append(arr)

    if args.lowest:
        codecs.sort(key=lambda x: x[2])
        codecs = [codecs[0]]
    elif args.highest:
        codecs.sort(key=lambda x: x[2], reverse=True)
        codecs = [codecs[0]]

    unique_codecs = list(set(codecs))
    for codec in unique_codecs:
        added_something = False
        temp_MPD = "\t\t" + '<AdaptationSet mimeType="' + codec[0] + '" codecs="' + codec[1] + '">' + "\n"
        for profile in profiles:
            if (profiles[profiles.index(profile)].get("added") == True):
                continue

            if (codec[0] == profile["mime_type"] and codec[1] == profile["audio_codec"]):
                added_something = True
                print("Adding audio profile " + str(profile["id"]) + " to MPD")
                temp_MPD = temp_MPD + "\t\t\t" + '<Representation id="' + str(profile["id"]) + '" bandwidth="' + str(profile["max_bitrate"]) + '">' + "\n"

                base = str(obj["segment_template"])
                base = base[:base.rfind("{{profile_id}}/") + 15]
                base = base.replace("{{profile_id}}", str(profile["id"]))
                base = base.replace("&", "&amp;")
                temp_MPD = temp_MPD + "\t\t\t\t" + '<BaseURL>' + base + '</BaseURL>' + "\n"

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
                temp_MPD = temp_MPD + "\t\t\t\t" + '<SegmentTemplate media="' + media + '" initialization="' + init + '" duration="' + str(segment_length_in_milliseconds) + '" startNumber="0" timescale="' + str(timescale) + '">' + "\n"

                #Final Segment Timeline format
                '''
                <SegmentTimeline>
                    <S t="0" d="4" r="3088"/>
                </SegmentTimeline>
                '''
                temp_MPD = temp_MPD + "\t\t\t\t\t" + '<SegmentTimeline>' + "\n"
                temp_MPD = temp_MPD + "\t\t\t\t\t\t" + '<S t="0" d="' + str(segment_length_in_seconds) + '" r="' + str(int(duration_in_seconds / segment_length_in_seconds)) + '"/>' + "\n"
                temp_MPD = temp_MPD + "\t\t\t\t\t" + '</SegmentTimeline>' + "\n"


                temp_MPD = temp_MPD + "\t\t\t\t" + '</SegmentTemplate>' + "\n"
                temp_MPD = temp_MPD + "\t\t\t" + '</Representation>' + "\n"

                profiles[profiles.index(profile)]["added"] = True

        if added_something:
            MPD = MPD + temp_MPD
            MPD = MPD + "\t\t" + '</AdaptationSet>' + "\n\n"
    
    return MPD

def make_subtitle_adaptation_sets(obj: dict):
    MPD = ""
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

    return MPD

def make_mpd(obj: dict, args: argparse.Namespace):
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
    if not args.audio_only and not args.sub_only:
        MPD = MPD + make_video_adaptation_set(obj, args)

    # Audio next
    if not args.video_only and not args.sub_only:
        MPD = MPD + make_audio_adaptation_set(obj, args)

    # Subtitle example
    '''
    <AdaptationSet mimeType="text/vtt" lang="en-US">
    <Representation id="subtitle_eng" mimeType="text/vtt" codecs="wvtt" bandwidth="0">
        <BaseURL>https://subtitles.spotifycdn.com/subtitles/v1/origins/b1acc6dba4d449dcf7a71659d3fabea2/sources/dbdff182c8ea58b4aa22f93856acdc13/en-US.webvtt</BaseURL>
    </Representation>
    </AdaptationSet>
    '''
    # Subtitles last
    if not args.video_only and not args.audio_only:
        MPD = MPD + make_subtitle_adaptation_sets(obj)

    # MPD end
    MPD = MPD + "\t" + '</Period>' + "\n"
    MPD = MPD + '</MPD>'

    return MPD

def main():
    parser = argparse.ArgumentParser(description='Convert JSON video manifest to DASH MPD')
    parser.add_argument('-i', '--input', help='Input JSON file', type=str, required=True)
    parser.add_argument('-o', '--output', help='Output MPD file', type=str, required=True)
    parser.add_argument('-vo', '--video_only', help='Only include video', action='store_true')
    parser.add_argument('-ao', '--audio_only', help='Only include audio', action='store_true')
    parser.add_argument('-so', '--sub_only', help='Only include subtitles', action='store_true')
    parser.add_argument('--lowest', help='Only include lowest bitrate', action='store_true')
    parser.add_argument('--highest', help='Only include highest bitrate', action='store_true')
    parser.add_argument('--avc_only', help='Only include AVC', action='store_true')
    parser.add_argument('--vp9_only', help='Only include VP9', action='store_true')
    parser.add_argument('--print_mpd', help='Print MPD to console', action='store_true')
    args = parser.parse_args()

    if args.input is None:
        print("Please specify an input file")
        exit(1)

    try:
        obj = read_json_file(args.input)
    except:
        print("Could not read input file")
        exit(1)

    if args.output is None:
        if args.print_mpd:
            print("Please specify an output file or print to console")
            exit(1)

        if os.path.exists("output.mpd"):
            print("Output file already exists. Overwrite? (y/n)")
            overwrite = input()
            if overwrite == "y":
                os.remove("output.mpd")
            else:
                exit(1)

    if (args.video_only and args.audio_only) or (args.video_only and args.sub_only) or (args.audio_only and args.sub_only):
        print("Please only specify one of video_only, audio_only, or sub_only")
        exit(1)

    if (args.lowest and args.highest):
        print("Please only specify one of lowest or highest")
        exit(1)

    if (args.avc_only and args.vp9_only):
        print("Please only specify one of avc_only or vp9_only")
        exit(1)

    obj = read_json_file(args.input)
    result_mpd = make_mpd(obj, args)
    if args.print_mpd:
        print(result_mpd)

    if args.output is not None:
        save_text_file(args.output, result_mpd)

if __name__ == "__main__":
    main()