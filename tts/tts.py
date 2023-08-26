from google.cloud import texttospeech

class TTS(object):
  def __init__(self, male: bool):
    """
    Initialize TTS of given gender. 

    Args:
        male (bool): male if True, female otherwise. 
    """
    # Instantiates a client
    self.client = texttospeech.TextToSpeechClient()
    
    # Build the voice request, select ko-KR and Wavenet option. 
    self.voice_param = texttospeech.VoiceSelectionParams(
      language_code="ko-KR", 
      name="ko-KR-Wavenet-D" if male else "ko-KR-Wavenet-A",
      ssml_gender=texttospeech.SsmlVoiceGender.MALE if male else texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    self.audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.MP3, 
      speaking_rate=1.15
    )
  
  def read(self, text: str, audio_name: str):
    """
    Synthesize audio for given text and save it as mp3 file. 
    
    Args:
        text (str): text to be synthesized to speech. 
        audio_name (str): name of the mp3 file
        
    Return:
        None
    """
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = self.client.synthesize_speech(
      input=synthesis_input, voice=self.voice_param, audio_config=self.audio_config
    )

    # The response's audio_content is binary.
    with open(audio_name + ".mp3", "wb") as out:
      # Write the response to the output file.
      out.write(response.audio_content)
      print('Audio content written to file "' + audio_name + '.mp3"')
