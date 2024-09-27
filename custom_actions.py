from transformers import pipeline
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionMusicTheoryAnswer(Action):
    def name(self) -> str:
        return "action_music_theory_answer"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Initialize transformers model
        intent = tracker.latest_message['intent'].get('name')
        entities = tracker.latest_message['entities']
        question = tracker.latest_message.get('text')
        model = pipeline('question-answering')
        context = "In music theory, a major scale is a diatonic scale."
        result = model(question=question, context=context)

        

        if intent == "ask_scale":
            scale = next(e for e in entities if e['entity'] == 'scale_type')['value']
            dispatcher.utter_message(text=f"The {scale} scale consists of...")

        elif intent == "ask_chord":
            chord = next(e for e in entities if e['entity'] == 'chord_type')['value']
            dispatcher.utter_message(text=f"A {chord} chord is built using...")

        else :
            dispatcher.utter_message(text=f"Answer: {result['answer']}")
        return []
