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
        root_note = next(tracker.get_latest_entity_values("root_note"), None)

        scale_info = {
            "major scale": "A major scale is a diatonic scale that ascends by whole-steps (W) and half-steps (H) in this specific pattern: W-W-H-W-W-W-H.",
            "minor scale": "A minor scale has three types: natural, harmonic, and melodic. The natural minor scale ascends by whole-steps (W) and half-steps (H) in this specific pattern: W-H-W-W-H-W-W. The harmonic minor scale is the same as the natural minor, but raises the 7th. The melodic minor scale ascends with the 6th and 7th notes both raised, but descends as a natural minor.",
            "chromatic": "A chromatic scale is a twelve-tone scale that includes every pitch in an octave, each a semitone apart.",
            "pentatonic": "A pentatonic scale is a five-note scale commonly used in blues, rock, and jazz music. There are two types of pentatonic scales: major and minor."
        }

        major_scale_notes = {
            "C" : ["C", "D", "E", "F", "G", "A", "B", "C"],
            "C sharp" : ["C#", "D#", "E#", "F#", "G#", "A#", "B#", "C#"],
            "D flat" : ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C", "Db"],
            "D" : ["D", "E", "F#", "G", "A", "B", "C#", "D"],
            "E flat" : ["Eb", "F", "G", "Ab", "Bb", "C", "D", "Eb"],
            "E" : ["E", "F#", "G#", "A", "B", "C#", "D#", "E"],
            "F" : ["F", "G", "A", "Bb", "C", "D", "E", "F"],
            "F#" : ["F#", "G#", "A#", "B", "C#", "D#", "E#", "F#"],
            "Gb" : ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F", "Gb"],
            "G" : ["G", "A", "B", "C", "D", "E", "F#", "G"],
            "Ab" : ["Ab", "Bb", "C", "Db", "Eb", "F", "G", "Ab"],
            "A" : ["A", "B", "C#", "D", "E", "F#", "G#", "A"],
            "Bb" : ["Bb", "C", "D", "Eb", "F", "G", "A", "Bb"],
            "B" : ["B", "C#", "D#", "E", "F#", "G#", "A#", "B"],
            "Cb" : ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb", "Cb"],
        }
        if root_note and scale:
            if scale == "major scale" and root_note in major_scale_notes:
                scale_notes = major_scale_notes[root_note]
            else:
                scale_notes = None
            if scale_notes:
                msg = f"The notes of a {root_note} {scale} are: {', '.join(scale_notes)}."
        elif scale and scale.lower() in scale_info:
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
        root_note = next(tracker.get_latest_entity_values("root_note"), None)

        chord_info = {
            "major chord": "A major triad consists of the root, major third, and perfect fifth. For example, a C major triad consists of C, E, and G.",
            "minor chord": "A minor triad consists of the root, minor third, and perfect fifth. For example, a C minor triad consists of C, E flat, and G.",
            "diminished chord": "A diminished triad consists of the root, minor third, and diminished fifth. For example, a C diminished triad consists of C, E flat, and G flat.",
            "augmented chord": "An augmented triad consists of the root, major third, and augmented fifth. For example, a C augmented triad consists of C, E, and G sharp.",
            "major seventh chord": "A major seventh chord consists of the root, major third, perfect fifth, and major seventh. For example, a C major seventh chord consists of C, E, G, and B.",
            "minor seventh chord": "A minor seventh chord consists of the root, minor third, perfect fifth, and minor seventh. For example, a C minor seventh chord consists of C, E flat, G, and B flat.",
            "dominant seventh chord": "A dominant seventh chord consists of the root, major third, perfect fifth, and minor seventh. For example, a C dominant seventh chord consists of C, E, G, and B flat.",
            "half-diminished seventh chord": "A half-diminished seventh chord consists of the root, minor third, diminished fifth, and minor seventh. For example, a C half-diminished seventh chord consists of C, E flat, G flat, and B flat.",
            "diminished seventh chord": "A diminished seventh chord consists of the root, minor third, diminished fifth, and diminished seventh. For example, a C diminished seventh chord consists of C, E flat, G flat, and B double flat."
        }
        major_chord_notes = {
            "C" : ["C", "E", "G"],
            "C sharp" : ["C#", "E#", "G#"],
            "D flat" : ["Db", "F", "Ab"],
            "D sharp" : ["D#", "F*", "A#"],
            "E flat" : ["Eb", "G", "Bb"],
            "D" : ["D", "F#", "A"],
            "E" : ["E", "G#", "B"],
            "E sharp" : ["E#", "G*", "B#"],
            "F flat" : ["Fb", "Ab", "Cb"],
            "F" : ["F", "A", "C"],
            "F sharp" : ["F#", "A#", "C#"],
            "G flat" : ["Gb", "Bb", "Db"],
            "G" : ["G", "B", "D"],
            "G sharp" : ["G#", "B#", "D#"],
            "A flat" : ["Ab", "C", "Eb"],
            "A" : ["A", "C#", "E"],
            "A sharp" : ["A#", "C*", "E#"],
            "B flat" : ["Bb", "D", "F"],
            "B" : ["B", "D#", "F#"],
            "B sharp" : ["B#", "D*", "F*"],
            "C flat" : ["Cb", "Eb", "Gb"],
        }

        minor_chord_notes = {
            "C" : ["C", "Eb", "G"],
            "C sharp" : ["C#", "E", "G#"],
            "D flat" : ["Db", "Fb", "Ab"],
            "D sharp" : ["D#", "F#", "A#"],
            "E flat" : ["Eb", "Gb", "Bb"],
            "D" : ["D", "F", "A"],
            "E" : ["E", "G", "B"],
            "E sharp" : ["E#", "G#", "B#"],
            "F flat" : ["Fb", "Abb", "Cb"],
            "F" : ["F", "Ab", "C"],
            "F sharp" : ["F#", "A", "C#"],
            "G flat" : ["Gb", "Bbb", "Db"],
            "G" : ["G", "Bb", "D"],
            "G sharp" : ["G#", "B", "D#"],
            "A flat" : ["Ab", "Cb", "Eb"],
            "A" : ["A", "C", "E"],
            "A sharp" : ["A#", "C#", "E#"],
            "B flat" : ["Bb", "Db", "F"],
            "B" : ["B", "D", "F#"],
            "B sharp" : ["B#", "D#", "F*"],
            "C flat" : ["Cb", "Ebb", "Gb"],
        }

        augmented_chord_notes = {
            "C" : ["C", "E", "G#"],
            "C sharp" : ["C#", "E#", "G*"],
            "D flat" : ["Db", "F", "A"],
            "D sharp" : ["D#", "F*", "A*"],
            "E flat" : ["Eb", "G", "B"],
            "D" : ["D", "F#", "A#"],
            "E" : ["E", "G#", "B#"],
            "E sharp" : ["E#", "G*", "B*"],
            "F flat" : ["Fb", "Ab", "C"],
            "F" : ["F", "A", "C#"],
            "F sharp" : ["F#", "A#", "C*"],
            "G flat" : ["Gb", "Bb", "D"],
            "G" : ["G", "B", "D#"],
            "G sharp" : ["G#", "B#", "D*"],
            "A flat" : ["Ab", "C", "E"],
            "A" : ["A", "C#", "E#"],
            "A sharp" : ["A#", "C*", "E*"],
            "B flat" : ["Bb", "D", "F#"],
            "B" : ["B", "D#", "F*"],
            "B sharp" : ["B#", "D*", "F#*"],
            "C flat" : ["Cb", "Eb", "G"],
        }

        diminished_chord_notes = {
            "C" : ["C", "Eb", "Gb"],
            "C sharp" : ["C#", "E", "G"],
            "D flat" : ["Db", "Fb", "Abb"],
            "D sharp" : ["D#", "F#", "A"],
            "E flat" : ["Eb", "Gb", "Bbb"],
            "D" : ["D", "F", "Ab"],
            "E" : ["E", "G", "Bb"],
            "E sharp" : ["E#", "G#", "B"],
            "F flat" : ["Fb", "Abb", "Cbb"],
            "F" : ["F", "Ab", "Cb"],
            "F sharp" : ["F#", "A", "C"],
            "G flat" : ["Gb", "Bbb", "Dbb"],
            "G" : ["G", "Bb", "Db"],
            "G sharp" : ["G#", "B", "D"],
            "A flat" : ["Ab", "Cb", "Ebb"],
            "A" : ["A", "C", "Eb"],
            "A sharp" : ["A#", "C#", "E"],
            "B flat" : ["Bb", "Db", "Fb"],
            "B" : ["B", "D", "F"],
            "B sharp" : ["B#", "D#", "F#"],
            "C flat" : ["Cb", "Ebb", "Gbb"],
        }

        if root_note and chord:
            if chord == "major chord" and root_note in major_chord_notes:
                chord_notes = major_chord_notes[root_note]
            elif chord == "minor chord" and root_note in minor_chord_notes:
                chord_notes = minor_chord_notes[root_note]
            elif chord == "augmented chord" and root_note in augmented_chord_notes:
                chord_notes = augmented_chord_notes[root_note]
            elif chord == "diminished chord" and root_note in diminished_chord_notes:
                chord_notes = diminished_chord_notes[root_note]
            else:
                chord_notes = None
            if chord_notes:
                msg = f"The notes of a {root_note} {chord} are: {', '.join(chord_notes)}."
        elif chord and chord.lower() in chord_info:
            msg = f"{chord.capitalize()}: {chord_info[chord.lower()]}"
        elif not chord:
            msg = "A chord is a set of notes that are played simultaneously to create harmony. Some types of chords include triads (stacks of three notes) and seventh chords (stacks of four notes)."
        else:
            msg = "I don't recognize that chord as I am still under development. Please provide a simpler chord type (ie one of the basic triads or seventh chords)."
        
        dispatcher.utter_message(text=str(msg))
        return []
