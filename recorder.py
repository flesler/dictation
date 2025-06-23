from RealtimeSTT import AudioToTextRecorder
import runner
import microphone
import system
from system import Sounds
import tray
from tray import Colors

recorder = None

def start():
  global recorder
  device_index = microphone.get_device_index()
  args = system.args
  lang = args.lang
  size = args.size
  quant = args.quant
  wakeword = args.wakeword
  root = system.abs_path("./downloads")
  print(f"Starting recorder with lang: {lang}, size: {size}, quant: {quant}, wakeword: {wakeword}")
  model = size
  if lang == "en" and not '-' in model:
    model = f"{model}.en"
  if quant and quant != 'none':
    model = f"{root}/{model}-{quant}"
  initial_prompt = prompt if lang == 'en' else None
  recorder = AudioToTextRecorder(
    download_root=root,
    model=model,
    language=lang, # None is Auto
    # device="cpu", # "cuda",
    compute_type="default", # "auto", # "int8_float16",
    input_device_index=device_index,
    spinner=False, # Default True
    no_log_file=True,
    start_callback_in_new_thread=True,
    min_gap_between_recordings=0.01, # Default 1
    min_length_of_recording=0.01, # Default 1
    # This is key, flushes the buffer
    post_speech_silence_duration=0.5, # Default 0.2
    initial_prompt=prompt,
    normalize_audio=True,
    silero_sensitivity=0.4,
    silero_use_onnx=True,
    silero_deactivity_detection=True,
    webrtc_sensitivity=3,
    wake_words="jarvis" if wakeword else None,
    wakeword_backend='pvporcupine' if wakeword else None,
    wake_words_sensitivity=0.8,
    wake_word_timeout=4,
    wake_word_buffer_duration=0.1, # Default 0.1
    # Must be 0 to auto-activate but then we need an actual timeout
    wake_word_activation_delay=0,
    on_wakeword_detected=_on_wakeword,
    on_wakeword_timeout=_on_wakeword_timeout,
  )

def stop():
  global recorder
  if recorder:
    # recorder.stop()
    recorder.shutdown()
  recorder = None

def monitor(callback):
  global recorder
  while is_running():
    text = recorder.text()
    if text:
      text = callback(text) or text
      # Might help with short sub-sentences dictated slowly
      if recorder:
        recorder.initial_prompt += text

def is_running():
  return recorder is not None

def text():
  # Just for testing
  return recorder.text()

def _on_wakeword():
  # FIXME: Seems like it might cut if processing or buffering takes too long, maybe set delay to 0 on on_vad_detect_start and restore on on_vad_detect_stop
  # If not set, it ends after the first buffer, if set on start, starts recording immediately
  recorder.wake_word_activation_delay = recorder.wake_word_timeout
  runner.reset()
  system.play(Sounds.START)
  tray.set(Colors.ACTIVE)

def _on_wakeword_timeout():
  if recorder.wake_word_activation_delay:
    # Patch a bug, it calls this twice per stop when nothing was said
    recorder.wake_word_activation_delay = 0
    system.play(Sounds.STOP)
    tray.set(Colors.INACTIVE)

# Not an LLM prompt per se, it might help bias the model
prompt = """You receive dictation that includes both regular text and spoken keyboard shortcuts or commands.
Transcribe spoken shortcuts and commands exactly as you hear them, using words like enter, control a, control alt v, comma, period, etc.
"""