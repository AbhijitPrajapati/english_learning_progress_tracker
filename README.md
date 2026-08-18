# english_learning_progress_tracker

English learners often face no shortage of feedback in regards to their speaking ability. However, prioritizing recurring mistakes amidst large volumes of feedback is a prevailing issue among many learning to speak. This application is a practical tool for English learners to not only recieve grammatical feedback, but also repair recurring issues overtime. Users record short samples of speech, which are transcribed and analyzed for grammatical inaccuracies. A persistant log of errors is constructed overtime, which the system uses to provide a long-term overview of users' improvement through error trends across multiple timeframes and error categories.

# Features

## User Authentication

- Basic user authentication
- Access to personal error analytics and speech history

## Audio Procesing

- Audio submission
- Transcription
- Grammer analysis
- Speech storage

## Grammer Analysis

Error Information:
- Original text
- Corrected text
- Error category
- Explanation 
- Timestamp

## Analytics

- Multiple timeframes: all-time, yearly, monthly, weekly
- Total errors and speeches
- Error distribution
- Error frequency graph by category

# Technical Backend Architecture

- FastAPI
- Faster-whisper (local audio transcription)
- Open AI API (grammar analysis)
- PostgreSQL