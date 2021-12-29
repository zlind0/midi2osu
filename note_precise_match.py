#%%
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

TITLE='firebird'
ST=0
LIM=20
STFT_WINLEN=2048
NFFT=4096
SAMPLE_RATE=44100
STFT_WINDOW_TIME=(STFT_WINLEN/4)/SAMPLE_RATE



NOTE_NAME = np.array([""]*12+["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G2#","A2","A2#","B2","C3","C3#","D3","D3#","E3","F3","F3#","G3","G3#","A3","A3#","B3","C4","C4#","D4","D4#","E4","F4","F4#","G4","G4#","A4","A4#","B4","C5","C5#","D5","D5#","E5","F5","F5#","G5","G5#","A5","A5#","B5","C6","C6#","D6","D6#","E6","F6","F6#","G6","G6#","A6","A6#","B6","C7","C7#","D7","D7#","E7","F7","F7#","G7","G7#","A7","A7#","B7","C8","C8#","D8","D8#","E8","F8","F8#","G8","G8#","A8","A8#","B8","Beyond B8"])

NOTE_FREQ = np.array([0]*12+[16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96	,27.50	,29.14	,30.87	,32.70	,34.65	,36.71	,38.89	,41.20	,43.65	,46.25	,49.00	,51.91	,55.00	,58.27	,61.74	,65.41	,69.30	,73.42	,77.78	,82.41	,87.31	,92.50	,98.00	,103.83	,110.00	,116.54	,123.47	,130.81	,138.59	,146.83	,155.56	,164.81	,174.61	,185.00	,196.00	,207.65	,220.00	,233.08	,246.94	,261.63	,277.18	,293.66	,311.13	,329.63	,349.23	,369.99	,392.00	,415.30	,440.00	,466.16	,493.88	,523.25	,554.37	,587.33	,622.25	,659.26	,698.46	,739.99	,783.99	,830.61	,880.00	,932.33	,987.77	,1046.50	,1108.73	,1174.66	,1244.51	,1318.51	,1396.91	,1479.98	,1567.98	,1661.22	,1760.00	,1864.66	,1975.53	,2093.00	,2217.46	,2349.32	,2489.02	,2637.02	,2793.83	,2959.96	,3135.96	,3322.44	,3520.00	,3729.31	,3951.07	,4186.01	,4434.92	,4698.64	,4978.03	,5274.04	,5587.65	,5919.91	,6271.93	,6644.88	,7040.00	,7458.62	,7902.13,8000])

print(librosa.__version__)
y, sr=librosa.load(f'{TITLE}.mp3', sr=SAMPLE_RATE, duration=LIM-ST, offset=ST)
print(y.shape)

#%%

S = np.abs(librosa.stft(y, n_fft=NFFT, win_length=STFT_WINLEN))
print(S.shape)

# %%
import pretty_midi
midi_data = pretty_midi.PrettyMIDI(f'{TITLE}.mid')

note_times=[]
note_ends=[]
note_freq_pitches=[]
note_pitches=[]
for instrument in midi_data.instruments:
    for note in instrument.notes:
        if note.start<LIM:
            print(note.pitch, NOTE_NAME[note.pitch], NOTE_FREQ[note.pitch], note.start, note.end)
            note_times.append(note.start-ST)
            note_ends.append(note.end-ST)
            while note.pitch<60:
                note.pitch+=12
            note_pitches.append(note.pitch)
            note_freq_pitches.append(NOTE_FREQ[note.pitch])

# %%
# fig, ax = plt.subplots()
# img = librosa.display.specshow(librosa.amplitude_to_db(S,
#                                                        ref=np.max),
#                                y_axis='log', x_axis='time', ax=ax, sr=SAMPLE_RATE, hop_length=STFT_WINLEN/4)
# ax.set_title('Power spectrogram')

# fig.colorbar(img, ax=ax, format="%+2.0f dB")
# ax.plot(note_times, note_freq_pitches,"x", color="#FFFFFF")
# ax.plot(note_ends, note_freq_pitches,"x", color="#00FF00")
# plt.savefig('stft.pdf')

# %%
db = librosa.amplitude_to_db(S,ref=np.max)
db.shape
fft_freqs = librosa.fft_frequencies(sr=sr, n_fft=NFFT)
NOTE_FFT_ROW=[]
for note in NOTE_FREQ:
    NOTE_FFT_ROW.append(np.argmin(np.abs(fft_freqs-note)))
for idx, note in enumerate(NOTE_FFT_ROW):
    print(idx, note, NOTE_NAME[idx], NOTE_FREQ[idx])

#%%

from matplotlib.pyplot import figure
from scipy.signal import argrelextrema

note_idx=1
argrelextrema_order=10 # define how many points to use for the argrelextrema
harmonics=[0.5,1,2,4]
note_shifts=[0,12,24,36]

print("Note info:", note_pitches[note_idx], note_freq_pitches[note_idx], NOTE_NAME[note_pitches[note_idx]])
note_harmonics=[h*note_freq_pitches[note_idx] for h in harmonics]
print("Harmonic frequencies:", note_harmonics)

# this is ampllitude of all harmonic frequencies
freq_amplitude=np.zeros(S.shape[1])
for shift in note_shifts:
    freq_amplitude+=S[NOTE_FFT_ROW[note_pitches[note_idx]]]

# this is the overall amplitude of the sound
sum_amp=np.sum(S, axis=0)
sum_amp_gradient=np.gradient(sum_amp)
potential_note_times_by_gradient = argrelextrema(sum_amp_gradient, np.greater, order=argrelextrema_order)
potential_note_times_by_gradient = np.array(potential_note_times_by_gradient) * STFT_WINDOW_TIME + ST

# same_pitch_times contains the times when the note is played at the same pitch
same_pitch_times=[]
for idx, _pitch in enumerate(note_pitches):
    if _pitch == note_pitches[note_idx]:
        same_pitch_times.append(note_times[idx]+ST)

# solve potential notes using overall amplitude
potential_note_times = argrelextrema(sum_amp, np.greater, order=argrelextrema_order) 
potential_note_times = np.array(potential_note_times) * STFT_WINDOW_TIME + ST

#solve potential same pitch notes using pitch amplitude percentage
potential_note_times_by_pitch = argrelextrema(freq_amplitude/sum_amp, np.greater, order=argrelextrema_order)
potential_note_times_by_pitch = np.array(potential_note_times_by_pitch) * STFT_WINDOW_TIME + ST

print(potential_note_times_by_pitch)

#%%
figure(figsize=(40, 20), dpi=80)
# red dot is the time of note in midi file
# blue dot is the potential notes
plt.subplot(411)
plt.plot(np.arange(ST,LIM,(LIM-ST)/db.shape[1]), sum_amp)
plt.title(f"OVERALL_AMPLITUDE_VALUE FOR {NOTE_NAME[note_pitches[0]]}")
plt.plot(potential_note_times,[0]*len(potential_note_times), "X", color="#0000FF")
plt.xlim(ST,ST+LIM)

plt.subplot(412)
plt.plot(np.arange(ST,LIM,(LIM-ST)/db.shape[1]), sum_amp_gradient)
plt.title(f"OVERALL_AMPLITUDE_GRADIENT FOR {NOTE_NAME[note_pitches[0]]}")
plt.plot(potential_note_times_by_gradient,[0]*len(potential_note_times_by_gradient), "X", color="#00FF00")
plt.xlim(ST,ST+LIM)

plt.subplot(413)
plt.plot(np.arange(ST,LIM,(LIM-ST)/db.shape[1]), freq_amplitude)
plt.title(f"NOTE_HARMONIC_AMPLITUDE_VALUE FOR {NOTE_NAME[note_pitches[0]]}")
plt.plot(same_pitch_times,[0]*len(same_pitch_times), "X", color="#FF0000")
plt.plot(potential_note_times,[0]*len(potential_note_times), "X", color="#0000FF")
plt.xlim(ST,ST+LIM)


plt.subplot(414)
plt.plot(np.arange(ST,LIM,(LIM-ST)/db.shape[1]), freq_amplitude/sum_amp)
plt.title(f"NOTE_HARMONIC_AMPLITUDE_PERCENTAGE FOR {NOTE_NAME[note_pitches[0]]}")
plt.plot(note_times, [0.005]*len(note_times), "x", color="#444444")
plt.plot(potential_note_times,[0]*len(potential_note_times), "X", color="#0000FF")
plt.plot(potential_note_times_by_gradient,[-0.05]*len(potential_note_times_by_gradient), "X", color="#00FF00")
plt.plot(potential_note_times_by_pitch,[-0.025]*len(potential_note_times_by_pitch), "X", color="#00F0F0")

plt.plot(same_pitch_times,[0]*len(same_pitch_times), "X", color="#FF0000")
plt.xlim(ST,ST+LIM)
plt.savefig(f"note_db_analysis.pdf")
# %%
same_pitch_times
# %%

# %%
