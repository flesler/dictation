from RealtimeSTT import AudioToTextRecorder
import runner
import microphone
import system

recorder = None

def start():
  global recorder
  lang = system.args.lang or 'en'
  polish = system.args.polish or False
  size = 'base' # 'small' # 'tiny' # 'distil-large-v3' #
  model = size
  if lang == "en" and not '-' in size:
    model = f"{size}.en"
  print(f"Starting recorder with lang: {lang}, size: {size}, polish: {polish}, model: {model}")
  recorder = AudioToTextRecorder(
    download_root=system.abs_path("./downloads"),
    model=model,
    language=lang, # None is Auto
    compute_type="auto", # "int8_float16",
    input_device_index=microphone.get_device_index(),
    spinner=False, # Default True
    no_log_file=True,
    ensure_sentence_starting_uppercase=polish,
    ensure_sentence_ends_with_period=polish,
    start_callback_in_new_thread=True,
    enable_realtime_transcription=False, # False, # Default
    realtime_processing_pause=0.0, # Default 0.2
    use_main_model_for_realtime=True, # Change
    min_gap_between_recordings=0.0, # Default 1
    min_length_of_recording=0.0, # Default 1
    # This is key, flushes the buffer
    post_speech_silence_duration=0.2, # Default 0.2
    wake_words=None,
    initial_prompt=prompt,
    initial_prompt_realtime=prompt,
    normalize_audio=True,
    # silero_sensitivity=0.8,
    # silero_use_onnx=True,
    # silero_deactivity_detection=True,
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

# Not an LLM prompt per se, it might help bias the model
prompt = """You receive dictation that includes both regular text and spoken keyboard shortcuts or commands.
Transcribe spoken shortcuts and commands exactly as you hear them, using words like enter, control a, control alt v, comma, period, etc.
"""