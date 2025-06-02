from RealtimeSTT import AudioToTextRecorder
import runner
import microphone

recorder = None

def start(lang=None, size='tiny'):
  global recorder
  if lang == None:
    lang = 'en'
  print(f"Starting recorder with lang: {lang}, size: {size}")
  recorder = AudioToTextRecorder(
    model=f"{size}.en" if lang == "en" else size, # small.en
    language=lang, # "" is Auto
    compute_type="int8_float16",
    input_device_index=microphone.get_device_index(),
    spinner=False, # Default True
    no_log_file=True,
    start_callback_in_new_thread=True,
    enable_realtime_transcription=False, # False, # Default
    realtime_processing_pause=0.1, # Default 0.2
    use_main_model_for_realtime=True, # Change
    min_gap_between_recordings=0.0, # Default 1
    min_length_of_recording=0.0, # Default 1
    wake_words=None,
  )

def stop():
  global recorder
  recorder.shutdown()
  recorder = None

def monitor(callback):
  while is_running():
    recorder.text(callback)

def is_running():
  return recorder is not None
