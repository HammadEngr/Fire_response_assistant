from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict

# Import all responses from separate file
from responses import (
    HOUSE_KITCHEN, HOUSE_ELECTRICAL, HOUSE_BEDROOM, HOUSE_GARAGE, HOUSE_GAS, HOUSE_OTHER,
    BUILDING_INSIDE, BUILDING_OUTSIDE,
    FACTORY_WORKER, FACTORY_VISITOR, FACTORY_OUTSIDE,
    WAREHOUSE_LARGE, WAREHOUSE_SMALL,
    FOREST, DEFAULT_RESPONSE
)


# ============================================================
# HELPER FUNCTION
# ============================================================
def get_risk_level(is_critical: str, is_high: str, is_rising: str) -> str:
    """Determine risk level from yes/no answers."""
    if is_critical == "yes":
        return "critical"
    elif is_high == "yes":
        return "high"
    elif is_rising == "yes":
        return "rising"
    else:
        return "low"


# ============================================================
# FORM VALIDATION - SHARED MIXIN
# ============================================================
class RiskFormValidationMixin:
    """Shared validation logic for forms with risk questions."""

    def validate_house_location(
            self, slot_value:Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:
        return {"house_location":slot_value}


    def validate_is_critical(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value == "yes":
            return {
                "is_critical": "yes",
                "is_high": "yes",
                "is_rising": "yes"
            }
        return {"is_critical": slot_value}
    
    def validate_is_high(
            self, slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value == "yes":
            return {
                "is_high":"yes",
                "is_rising":"yes"
            }
        return {"is_high":slot_value}
    
    def validate_is_rising(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"is_rising": slot_value}


# ============================================================
# FORM VALIDATION CLASSES
# ============================================================
class ValidateHouseFireForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        print(f"==DEBUG== validate_house_fire_form TRIGGERED")
        return "validate_house_fire_form"


class ValidateFactoryOutsideForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_factory_outside_form"


class ValidateWarehouseSmallForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_warehouse_small_form"


class ValidateForestFireForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_forest_fire_form"


# ============================================================
# ROUTING ACTIONS
# ============================================================
class ActionRouteAfterSiteSelection(Action):
    """Route to appropriate form based on site_type."""

    def name(self) -> Text:
        return "action_route_after_site_selection"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        site_type = tracker.get_slot("site_type")
        
        if site_type == "house":
            return [FollowupAction("house_fire_form")]
        else:
            dispatcher.utter_message(text="Unknown site type. Please try again.")
            return [FollowupAction("site_selection_form")]


# ============================================================
# MAIN SUBMIT ACTION
# ============================================================
class ActionSubmitFireAssessment(Action):
    """Process form data and provide appropriate response."""
    print(f"==DEBUG== ActionSubmitFireAssessment Trigerred")

    def name(self) -> Text:
        return "action_submit_fire_assessment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Get all slots
        site_type = tracker.get_slot("site_type")
        house_location = tracker.get_slot("house_location")
        is_critical = tracker.get_slot("is_critical")
        is_high = tracker.get_slot("is_high")
        is_rising = tracker.get_slot("is_rising")

        # Get response
        response = self._get_response(
            site_type, house_location, 
            is_critical, is_high, is_rising
        )
        print(f"==DEBUG=={response}")

        # Send response
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="🆘 Emergency Helpline: 112\n\nStay safe!")

        # Reset all slots
        return [
            SlotSet("site_type", None),
            SlotSet("house_location", None),
            SlotSet("is_critical", None),
            SlotSet("is_high", None),
            SlotSet("is_rising", None)
        ]

    def _get_response(
        self, site_type, house_location,
        is_critical, is_high, is_rising
    ) -> str:

        # ----- HOUSE -----
        if site_type == "house":
            risk = get_risk_level(is_critical, is_high, is_rising)
            print(f"DEBUG==risk={risk}, house_location={house_location}")
            location_map = {
                "kitchen": HOUSE_KITCHEN,
                "electrical": HOUSE_ELECTRICAL,
                "bedroom": HOUSE_BEDROOM,
                "garage": HOUSE_GARAGE,
                "gas_area": HOUSE_GAS,
                "other": HOUSE_OTHER
            }
            responses = location_map.get(house_location, HOUSE_OTHER)
            print(f"DEBUG===responses={responses}")
            return responses.get(risk, "Emergency! Call 112.")

        # ----- DEFAULT -----
        else:
            return DEFAULT_RESPONSE
        
class ActionResetSlots(Action):
    """Reset all slots at the start of every fire report."""

    def name(self) -> Text:
        return "action_reset_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return [
            SlotSet("site_type", None),
            SlotSet("house_location", None),
            SlotSet("is_critical", None),
            SlotSet("is_high", None),
            SlotSet("is_rising", None)
        ]