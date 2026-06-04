from enum import Enum

class MoodType(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ENERGETIC = "energetic"
    CHILL = "chill"
    FOCUSED = "focused"
    ROMANTIC = "romantic"
    ANGRY = "angry"
    NOSTALGIC = "nostalgic"

class FeedItemType(str, Enum):
    USER_POST = "user_post"
    RECOMMENDATION = "recommendation"
    TRENDING = "trending"

class RecommendationType(str, Enum):
    DNA_MATCH = "dna_match"
    FRIEND_ACTIVITY = "friend_activity"
    AI_DJ = "ai_dj"
    MOOD_BASED = "mood_based"

class NotificationType(str, Enum):
    FOLLOW = "follow"
    LIKE = "like"
    COMMENT = "comment"
    DJ_MIX = "dj_mix"
    SOULMATE_FOUND = "soulmate_found"

class ModerationActionType(str, Enum):
    REPORT = "report"
    BLOCK = "block"
    MUTE = "mute"
