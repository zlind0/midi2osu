import pretty_midi
import random, sys, os

if len(sys.argv) < 2:
    print("Usage: python3 midi2osu.py <basename>\nNote that both .mid and .mp3 files should all be present.")
    exit(1)
TITLE=sys.argv[1]

if not os.path.exists(TITLE+".mid"):
    print(f"{TITLE}.mid not found.")
    exit(1)

if not os.path.exists(TITLE+".mp3"):
    print(f"{TITLE}.mp3 not found.")
    exit(1)

unify=False
single_track=True
midi_data = pretty_midi.PrettyMIDI(f'{TITLE}.mid')
# print(midi_data.__dict__)
# print(midi_data.time_signature_changes)
prefix="""osu file format v14


AudioFilename: TITLE.mp3
AudioLeadIn: 0
PreviewTime: 43174
Countdown: 1
SampleSet: Normal
StackLeniency: 0.7
Mode: 3
LetterboxInBreaks: 0
SpecialStyle: 0
WidescreenStoryboard: 1

[Editor]
DistanceSpacing: 0.9
BeatDivisor: 4
GridSize: 32
TimelineZoom: 2.1

[Metadata]
Title:TITLE
TitleUnicode:TITLE
Artist:Lind
ArtistUnicode:Lind
Creator:Lind
Version:Alpha
Source:
Tags:
BeatmapID:96072221
BeatmapSetID:96072221

[Difficulty]
HPDrainRate:4
CircleSize:4
OverallDifficulty:8
ApproachRate:10
SliderMultiplier:2
SliderTickRate:2

[TimingPoints]
0,500,4,2,0,0,1,0

[HitObjects]

""".replace('TITLE',TITLE)

def track_to_keys(note_seq,xrange=(0,512),yrange=(0,512), max_keys=4):
    # Note: start, end, pitch, velocity
    # TODO: add support for "holding" notes
    # TODO: deal with concurrent keys
    res=[]
    lastkey=-1
    lastpitch=0
    key_x_delta=(xrange[1]-xrange[0])/max_keys
    key_x_delta_2=int(key_x_delta/2)
    for note in note_seq:
        if note.pitch > lastpitch:
            lastkey=min(max_keys-1, lastkey+1)
        else:
            lastkey=max(0, lastkey-1)
        lastpitch=note.pitch
        x=int(lastkey*key_x_delta)+key_x_delta_2+xrange[0]
        y=random.randint(*yrange)
        t=int(note.start*1000)
        res.append((t,f"{x},{y},{t},1,0,0:0:0:0:"))
    return res

with open(f'test.osu','w') as f:
    f.write(prefix)
    print(f"INSTRUMENTS={len(midi_data.instruments)}")
    allres=[]
    for idx, instrument in enumerate(midi_data.instruments):
        idx=1-idx
        print(f"INSTRUNENT NOTES={len(instrument.notes)}")
        if unify or single_track:
            allres+=track_to_keys(instrument.notes)
        else: # assume the first track to be right hand notes
            allres+=track_to_keys(instrument.notes, xrange=(256*(idx), 256*(idx+1)), max_keys=2)
        if single_track: break
    allres=sorted(allres)
    f.write("\n".join((i[1] for i in allres)))

from zipfile import ZipFile
zipObj = ZipFile(f'{TITLE}.osz', 'w')
# Add multiple files to the zip
zipObj.write('test.osu')
zipObj.write(f'{TITLE}.mp3')
zipObj.close()


"""
Desired output format
Hit object syntax: x,y,time,type,hitSound,objectParams,hitSample

    x (Integer) and y (Integer): Position in osu! pixels of the object.
    time (Integer): Time when the object is to be hit, in milliseconds from the beginning of the beatmap's audio.
    type (Integer): Bit flags indicating the type of the object. See the type section.
    hitSound (Integer): Bit flags indicating the hitsound applied to the object. See the hitsounds section.
    objectParams (Comma-separated list): Extra parameters specific to the object's type.
    hitSample (Colon-separated list): Information about which samples are played when the object is hit. It is closely related to hitSound; see the hitsounds section. If it is not written, it defaults to 0:0:0:0:.

[HitObjects]
59,52,262,5,2,0:0:0:0:
73,131,539,1,0,0:0:0:0:
151,149,817,1,2,0:0:0:0:
140,229,1095,1,0,0:0:0:0:
65,268,1373,1,2,0:0:0:0:
79,347,1650,1,0,0:0:0:0:
199,284,1928,1,2,0:0:0:0:
140,229,2206,1,0,0:0:0:0:
163,357,2484,5,2,0:0:0:0:
287,336,2761,2,0,P|341:327|384:322,1,90
411,220,3317,1,0,0:0:0:0:
326,152,3595,2,0,P|316:205|311:242,1,90,2|0,0:0|0:0,0:0:0:0:
468,300,4150,5,2,0:0:0:0:
"""
