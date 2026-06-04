from textblob import TextBlob
from libs.shared.enums import Mood

class EmotionLogic:
    def analyze_text(self, text: str) -> Mood:
        """
        A simple heuristic based emotion analyzer using textblob polarity.
        In a real app, this would use an ML model.
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.5:
            return Mood.HAPPY
        elif polarity > 0.1:
            return Mood.ENERGETIC
        elif polarity < -0.1:
            return Mood.SAD
        else:
            return Mood.CHILL
