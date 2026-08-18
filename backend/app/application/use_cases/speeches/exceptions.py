from app.application.exceptions import ApplicationError


class SpeechNotFound(ApplicationError):
    pass


class AnalysisQuotaReached(ApplicationError):
    pass
