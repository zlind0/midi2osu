from mido import MidiFile 
from mido import Message, MidiTrack
# from MIDI import MIDIFile 
import pandas as pd
from midiutil import MIDIFile

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)
mid=MidiFile('test.mid')

f=open('out.txt','wb')
def print(st):
    f.write((str(st)+'\n').encode('utf-8'))

TPB=mid.ticks_per_beat
print(f"TPB = {TPB}")

TIME_TOTAL=0.0

NOTE_ON={}
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        # print(msg)
        if(msg.type == 'set_tempo'):
            print(f"BPM {msg.tempo}")
        if(msg.type == 'time_signature'):
            # TPB=msg.clocks_per_click*msg.notated_32nd_notes_per_beat
            print(f"TIME_SIG {msg.numerator}/{msg.denominator}")
        if(msg.type == 'note_on'):
            TIME_TOTAL+=msg.time
            if(msg.velocity>0):
                NOTE_ON[msg.note]=TIME_TOTAL
            else:
                print(f"NOTE {msg.note} TIME {NOTE_ON[msg.note]/TPB}-{TIME_TOTAL/TPB}")

    # if (not msg.is_meta):
        
    #     if (msg.type == 'note_on'):
    #         # how to convert msg.time to tick to fill in '?'
    #         track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=?))
    #     elif (msg.type == 'note_off'):
    #         # how to convert msg.time to tick to fill in '?'
    #         track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=?))
    #     elif (msg.type == 'program_change'):
    #         track.append(Message('program_change', program=msg.program, channel=msg.channel))

f.close()