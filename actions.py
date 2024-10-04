# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
version: "3.1"
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionScaleAnswer(Action):

    def name(self) -> Text:
        return "action_scale_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        scale = next(tracker.get_latest_entity_values("scale_type"), None)

        scale_info = {
             "major": "A major scale is a diatonic scale that ascends by whole-steps (W) and half-steps (H) in this specific pattern: W-W-H-W-W-W-H.",
            "minor": "A minor scale has three types: natural, harmonic, and melodic. The natural minor scale ascends by whole-steps (W) and half-steps (H) in this specific pattern: W-H-W-W-H-W-W. The harmonic minor scale is the same as the natural minor, but raises the 7th. The melodic minor scale ascends with the 6th and 7th notes both raised, but descends as a natural minor.",
            "chromatic": "A chromatic scale is a twelve-tone scale that includes every pitch in an octave, each a semitone apart.",
            "pentatonic": "A pentatonic scale is a five-note scale commonly used in blues, rock, and jazz music. There are two types of pentatonic scales: major and minor."
        }
        if scale and scale.lower() in scale_info:
            msg = f"{scale.capitalize()} scale: {scale_info[scale.lower()]}"
        elif not scale:
            msg = "I don't recognize that scale as I am still under development. Please provide a simpler scale type."
        
        #    msg = "A scale is a sequence of ascending notes with a specific pattern of whole (W) steps and half (H) steps. Different types of scales include major, minor, and pentatonic."
        dispatcher.utter_message(text=msg)
        return []
