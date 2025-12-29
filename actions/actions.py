from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

print(">>> Loading Education Flow <<<")

class ActionHandleFireEducationChapterChoice(Action):

    def name(self) -> Text:
        return "action_handle_fire_education_chapter_choice"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        chapter = tracker.get_slot("education_chapter")

        print(chapter)


        if chapter:
            chapter = chapter.lower().replace(" ", "_")
            if "basic" in chapter or "basics" in chapter:
                dispatcher.utter_message(response="utter_fire_basics")
            elif any(word in chapter for word in ["mitigation","avoid", "extinguish"]):
                dispatcher.utter_message(response="utter_fire_mitigation")
            elif "risk" in chapter or "assessment" in chapter:
                dispatcher.utter_message(response="utter_fire_risk_assessment_steps")
            else:
                dispatcher.utter_message(response="utter_general_education")
        else:
            dispatcher.utter_message(response="utter_fire_education")


        return []
