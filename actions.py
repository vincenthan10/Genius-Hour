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


        scale_info = {
            "major scale": "A major scale is a diatonic scale that ascends by whole-steps (W) and half-steps (H) in this specific pattern: W-W-H-W-W-W-H.",
            "minor scale": "A minor scale has three types: natural, harmonic, and melodic. The natural minor scale ascends by whole-steps (W) and half-steps (H) in this specific pattern: W-H-W-W-H-W-W. The harmonic minor scale is the same as the natural minor, but raises the 7th. The melodic minor scale ascends with the 6th and 7th notes both raised, but descends as a natural minor.",
            "chromatic": "A chromatic scale is a twelve-tone scale that includes every pitch in an octave, each a semitone apart.",
            "pentatonic": "A pentatonic scale is a five-note scale commonly used in blues, rock, and jazz music. There are two types of pentatonic scales: major and minor."
        }

        if scale and scale.lower() in scale_info:
            msg = f"{scale.capitalize()}: {scale_info[scale.lower()]}"
        elif not scale:
            msg = "A scale is sequence of notes with a specific pattern of whole (W) and half (H) steps. Different types of scales include major, minor, and pentatonic."
        else:
            msg = "I don't recognize that scale as I am still under development. Please provide a simpler scale type."
        
        dispatcher.utter_message(text=msg)
        return []


class ActionIntervalAnswer(Action):
    def name(self) -> Text:
        return "action_interval_answer"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        quality = next(tracker.get_latest_entity_values("quality"), None)
        distance = next(tracker.get_latest_entity_values("distance"), None)

        if quality and distance:
            interval_info = {
                "major": f"A major {distance} interval is the distance between the root note and the upper {distance} note in a major scale.",
                "minor": f"A minor {distance} interval is the distance between the root note and the upper {distance} note in a major scale, but the upper {distance} is lowered by a semitone.",
                "perfect": f"A perfect {distance} interval is the distance between the root note and the upper {distance} note in both major and minor scales.",
                "diminished": f"A diminished {distance} interval is the same as a minor {distance} interval, but the upper {distance} is lowered by a semitone.",
                "augmented": f"An augmented {distance} interval is the same as a major {distance} interval, but the upper {distance} is raised by a semitone."
            } 
        elif quality and not distance:
            interval_info = {
                "major": "A major interval is the distance between two notes in a major scale, used to describe seconds, thirds, sixths, and sevenths.",
                "minor": "A minor interval is one semitone lower than the corresponding major interval.",
                "perfect": "A perfect interval is the distance between two notes in both major and minor scales, used to describe unisons, fourths, fifths, and octaves.",
                "diminished": "A diminished interval is one semitone lower than a minor or perfect interval.",
                "augmented": "An augmented interval is one semitone higher than a major or a perfect interval."
            }
        

        if not quality and not distance:
            msg = "An interval is the distance between two notes in music. Different types of intervals include major, minor, perfect, augmented, and diminished."
        elif distance and not quality:
            msg = f"A {distance} interval is the distance between the root note and the {distance} note in a scale."
        else:
            msg = interval_info[quality.lower()]

        dispatcher.utter_message(text=str(msg))
        return []
    
class ActionChordAnswer(Action):
    def name(self) -> Text:
        return "action_chord_answer"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        chord = next(tracker.get_latest_entity_values("chord_type"), None)

        chord_info = {
            "major chord" or "major triad": "A major triad consists of the root, major third, and perfect fifth. For example, a C major triad consists of C, E, and G.",
            "minor chord" or "minor triad": "A minor triad consists of the root, minor third, and perfect fifth. For example, a C minor triad consists of C, E flat, and G.",
            "diminished chord" or "diminished triad": "A diminished triad consists of the root, minor third, and diminished fifth. For example, a C diminished triad consists of C, E flat, and G flat.",
            "augmented chord" or "augmented triad": "An augmentedd triad consists of the root, major third, and augmented fifth. For example, a C augmented triad consists of C, E, and G sharp.",
            "major seventh": "A major seventh chord consists of the root, major third, perfect fifth, and major seventh. For example, a C major seventh chord consists of C, E, G, and B.",
            "minor seventh": "A minor seventh chord consists of the root, minor third, perfect fifth, and minor seventh. For example, a C minor seventh chord consists of C, E flat, G, and B flat.",
            "dominant seventh": "A dominant seventh chord consists of the root, major third, perfect fifth, and minor seventh. For example, a C dominant seventh chord consists of C, E, G, and B flat.",
            "half-diminished seventh" or "half diminished seventh": "A half-diminished seventh chord consists of the root, minor third, diminished fifth, and minor seventh. For example, a C half-diminished seventh chord consists of C, E flat, G flat, and B flat.",
            "diminished seventh" or "fully-diminished seventh": "A diminished seventh chord consists of the root, minor third, diminished fifth, and diminished seventh. For example, a C diminished seventh chord consists of C, E flat, G flat, and B double flat."
        }

        if chord and chord.lower() in chord_info:
            msg = f"{chord.capitalize()}: {chord_info[chord.lower()]}"

        elif not chord:
            msg = "A chord is a set of notes that are played simultaneously to create harmony. Some types of chords include triads (stacks of three notes) and seventh chords (stacks of four notes)."

        else:
            msg = "I don't recognize that chord as I am still under development. Please provide a simpler chord type (ie one of the basic triads or seventh chords)."
        
        dispatcher.utter_message(text=str(msg))
        return []
