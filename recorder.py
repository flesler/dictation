from RealtimeSTT import AudioToTextRecorder
import pyautogui
import os
import sys
from devices import get_audio_device_index
import runner

def process_text(text):
  runner.process(text)
  # pyautogui.typewrite(text + " ")
  # print(text, file=sys.stderr)
  # print(text)

if __name__ == '__main__':
  # Cache in this directory
  os.environ["HF_HOME"] = os.path.abspath("./downloads")

  device_index = get_audio_device_index()
  # print("Wait until it says 'speak now'")
  lang = 'en' # es # ""
  with AudioToTextRecorder(
    model="tiny.en" if lang == "en" else "tiny", # small.en
    language=lang, # "" is Auto
    compute_type="int8_float16",
    input_device_index=device_index,
    spinner=False, # Default True
    no_log_file=True,
    start_callback_in_new_thread=True,
    enable_realtime_transcription=False, # Default
    use_main_model_for_realtime=True, # Change
    min_gap_between_recordings=0.1, # Default 1
    wake_words=None,
  ) as recorder:
    print('Ready')
    while True:
      recorder.text(process_text)
  # recorder.shutdown()