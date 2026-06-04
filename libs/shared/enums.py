from enum import Enum

class Mood(str, Enum):
    HAPPY = "HAPPY"
    SAD = "SAD"
    CHILL = "CHILL"
    ENERGETIC = "ENERGETIC"
    FOCUS = "FOCUS"

class FeedType(str, Enum):
    GLOBAL = "GLOBAL"
    FRIENDS = "FRIENDS"
    RECOMMENDED = "RECOMMENDED"

class RecommendationType(str, Enum):
    TRACK = "TRACK"
    PLAYLIST = "PLAYLIST"
    USER = "USER"

class EventTopic(str, Enum):
    USER_EVENTS = "user.events.v1"
    SOCIAL_EVENTS = "social.events.v1"
    MUSIC_EVENTS = "music.events.v1"
