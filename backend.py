import pyttsx3 as pyt

class Text_To_Audio(object):
    def __init__(self, voice, rate, pitch):
        self._engine = pyt.init()
        self.voice = voice
        self.rate = rate
        self.pitch = pitch

        if self.voice == 'male':
            self.voice = 0
        elif self.voice == 'female':
            self.voice = 1
        else:
            raise TypeError("Should be 'male' or 'female'")
        
        self._engine.setProperty("rate", self.rate)
        self._engine.setProperty("pitch", self.pitch)
        self._voices = self._engine.getProperty("voices")
        self._engine.setProperty("voice", self._voices[self.voice].id)
    
    def convert_to_audio(self, words, filename):
        try:
            self.words = words
            self.filename = filename
            self._engine.save_to_file(self.words, self.filename)
            self._engine.runAndWait()
        except Exception as e:
            return
        
tta = Text_To_Audio(voice='male', rate=150, pitch=0.8)