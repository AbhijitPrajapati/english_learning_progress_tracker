# from pydantic import BaseModel

# from app.domain.speech import MistakeCategory


# class DetectedMistake(BaseModel):
#     category: MistakeCategory
#     original_text: str
#     correction: str
#     explanation: str


# class MistakeFrequency(BaseModel):
#     category: MistakeCategory
#     opportunities: int
#     occurances: int


# class SpeechAnalysis(BaseModel):
#     frequencies: list[MistakeFrequency]
#     mistakes: list[DetectedMistake]
#     feedback: str
