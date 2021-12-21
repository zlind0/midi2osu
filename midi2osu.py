import pretty_midi

midi_data = pretty_midi.PrettyMIDI('test.mid')
# print(midi_data.__dict__)
# print(midi_data.time_signature_changes)

def track_to_keys(note_seq, max_keys=4):
    # Note: start, end, pitch, velocity
    # TODO: add support for "holding" notes
    pass


for instrument in midi_data.instruments:
    for note in instrument.notes:
        # print(note)
        pass


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
