from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

print(">>> Loading Custom Actions <<<")

class ActionHandleFireEducationChapterChoice(Action):

    def name(self) -> Text:
        return "action_handle_fire_education_chapter_choice"
    
    print(">>> Loaded: action_handle_fire_education_chapter_choice")

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

class ActionHandlImmediateThreatYes(Action):
    def name(self) -> Text:
        return "action_handle_immediate_threat_yes"
    
    print(">>> Loaded: action_handle_immediate_threat_yes")
    
    def run(
            self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        
        site = tracker.get_slot("incident_site")
        threat = tracker.get_slot("immediate_threat")

        print(site)
        print(threat)
        
        if threat != "none":
            if site == "house" and any (word in threat for word in ["heavy flames","heavy smoke", "entrapped", "burning embers"]):
                dispatcher.utter_message(response = "utter_handle_immediate_threat_house")
            elif site == "factory" and any (word in threat for word in ["heavy flames","heavy smoke", "entrapped", "burning embers"]):
                dispatcher.utter_message(response="utter_handle_immediate_threat_factory")
            elif site == "warehouse" and any (word in threat for word in ["heavy flames","heavy smoke", "entrapped", "burning embers"]):
                dispatcher.utter_message(response="utter_handle_immediate_threat_wh")
            elif site == "building" and any (word in threat for word in ["heavy flames","heavy smoke", "entrapped", "burning embers"]):
                dispatcher.utter_message(response="utter_handle_immediate_threat_building")
            elif site == "forest" and any (word in threat for word in ["heavy flames","heavy smoke", "entrapped", "burning embers"]):
                dispatcher.utter_message(response="utter_handle_immediate_threat_forest")
            else:
                dispatcher.utter_message(response="utter_handle_immediate_threat_general")
        else:
            if site == "house":
                dispatcher.utter_message(response="utter_handle_fire_responce_house")
            elif site == "factory":
                dispatcher.utter_message(response="utter_handle_fire_responce_factory")
            if site == "warehouse":
                dispatcher.utter_message(response="utter_handle_fire_responce_wh")
            if site == "building":
                dispatcher.utter_message(response="utter_handle_fire_responce_building")
            if site == "forest":
                dispatcher.utter_message(response="utter_handle_fire_responce_forest")
            else:
                dispatcher.utter_message(response="utter_handle_fire_responce_general")

        return []
        
