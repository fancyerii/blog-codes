import tensorflow as tf
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
from tensorflow.python.ops import io_ops
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat

desired_samples = 16000
wav_filename_placeholder_ = tf.placeholder(
    tf.string, [], name='wav_filename')
wav_loader = io_ops.read_file(wav_filename_placeholder_)
wav_decoder = contrib_audio.decode_wav(
    wav_loader, desired_channels=1, desired_samples=desired_samples)
# Allow the audio sample's volume to be adjusted.
foreground_volume_placeholder_ = tf.placeholder(
    tf.float32, [], name='foreground_volume')
scaled_foreground = tf.multiply(wav_decoder.audio,
                                foreground_volume_placeholder_)
# Shift the sample's start position, and pad any gaps with zeros.
time_shift_padding_placeholder_ = tf.placeholder(
    tf.int32, [2, 2], name='time_shift_padding')
time_shift_offset_placeholder_ = tf.placeholder(
    tf.int32, [2], name='time_shift_offset')
padded_foreground = tf.pad(
    scaled_foreground,
    time_shift_padding_placeholder_,
    mode='CONSTANT')
sliced_foreground = tf.slice(padded_foreground,
                             time_shift_offset_placeholder_,
                             [desired_samples, -1])

# Run the spectrogram and MFCC ops to get a 2D 'fingerprint' of the audio.
spectrogram = contrib_audio.audio_spectrogram(
    sliced_foreground,
    window_size=480,
    stride=160,
    magnitude_squared=True)

with tf.Session() as sess:
    f,sp,audio=sess.run([scaled_foreground,spectrogram,wav_decoder.audio], feed_dict=
    {wav_filename_placeholder_:"/home/lili/data/speech_dataset/no/0a2b400e_nohash_0.wav",
     foreground_volume_placeholder_:1.0,
     time_shift_padding_placeholder_:[[0,0],[0,0]],
     time_shift_offset_placeholder_:[0,0]
     })
    print(f.shape,sp.shape,audio.shape)