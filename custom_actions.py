from transformers import pipeline
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionMusicTheoryAnswer(Action):
    def name(self):
        return "action_music_theory_answer"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Initialize transformers model
        question = tracker.latest_message.get('text')
        model = pipeline('question-answering')
        context = "In music theory, a major scale is a diatonic scale."
        result = model(question=question, context=context)

        dispatcher.utter_message(text=f"Answer: {result['answer']}")
        return []