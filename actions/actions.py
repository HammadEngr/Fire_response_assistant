from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import UserUtteranceReverted

# RESPONSES
from responses import (
    HOUSE_KITCHEN, HOUSE_ELECTRICAL, HOUSE_BEDROOM, HOUSE_GARAGE, HOUSE_GAS, HOUSE_OTHER,
    BUILDING_INSIDE, BUILDING_OUTSIDE,
    FACTORY_WORKER, FACTORY_VISITOR, FACTORY_OUTSIDE,
    WAREHOUSE_LARGE, WAREHOUSE_SMALL,
    FOREST, DEFAULT_RESPONSE
)

# RISK LEVEL HELPER FUNCTION
def get_risk_level(is_critical: str, is_high: str, is_rising: str) -> str:
    # Determine risk level from yes/no answers
    if is_critical == "yes":
        return "critical"
    elif is_high == "yes":
        return "high"
    elif is_rising == "yes":
        return "rising"
    else:
        return "low"

# FORM VALIDATION HELPER
class RiskFormValidationMixin:
    
    #Shared validation logic
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


# FORM VALIDATION CLASSES
class ValidateSiteSelectionForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_site_selection_form"
    def validate_site_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        valid_sites = ["house", "building", "factory", "warehouse", "forest"]
        
        if slot_value in valid_sites:
            return {"site_type": slot_value}
        else:
            dispatcher.utter_message(text="Please select a valid location type from the options.")
            return {"site_type": None}

class ValidateHouseFireForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_house_fire_form"
    
    def validate_house_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        valid_locations = ["kitchen", "electrical", "bedroom", "garage", "gas_area", "other"]
        
        if slot_value in valid_locations:
            return {"house_location": slot_value}
        else:
            dispatcher.utter_message(text="Please select a valid location from the options.")
            return {"house_location": None}

class ValidateBuildingLoactionForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_building_location_form"

class ValidateFactoryLocationForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_factory_location_form"
    
class ValidateFactoryInsideForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_factory_inside_form"
    
    def validate_factory_role(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        valid_roles = ["worker", "visitor"]
        
        if slot_value in valid_roles:
            return {"factory_role": slot_value}
        else:
            dispatcher.utter_message(text="Please select either Worker or Visitor.")
            return {"factory_role": None}

class ValidateFactoryOutsideForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_factory_outside_form"
    
class ValidateWarehouseSizeForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_warehouse_size_form"
    
class ValidateWarehouseLargeForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_warehouse_large_form"


class ValidateWarehouseSmallForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_warehouse_small_form"
    
    def validate_warehouse_material(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        valid_materials = [
            "garments", "electrical", "mechanical", 
            "wood", "ceramics", "rubber", "chemicals", "mixed"
        ]
        
        if slot_value in valid_materials:
            return {"warehouse_material": slot_value}
        else:
            dispatcher.utter_message(text="Please select a valid material type from the options.")
            return {"warehouse_material": None}


class ValidateForestFireForm(RiskFormValidationMixin, FormValidationAction):
    def name(self) -> Text:
        return "validate_forest_fire_form"

# ROUTING ACTIONS AFTER EACH FORM
class ActionRouteAfterSiteSelection(Action):

    # Route to appropriate form based on site_type
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
        elif site_type == "building":
            print(f"==DEBUG==action_route_after_site_selection")
            return [FollowupAction("building_location_form")]
        elif site_type == "factory":
            return [FollowupAction("factory_location_form")]
        elif site_type == "warehouse":
            return [FollowupAction("warehouse_size_form")]
        elif site_type == "forest":
            return [FollowupAction("forest_fire_form")]
        else:
            dispatcher.utter_message(text="Unknown site type. Please try again.")
            return [FollowupAction("site_selection_form")]
        
class ActionRouteAfterFactoryLocation(Action):

    # Route to inside or outside factory form

    def name(self) -> Text:
        return "action_route_after_factory_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        factory_location = tracker.get_slot("factory_location")
        
        if factory_location == "inside":
            return [FollowupAction("factory_inside_form")]
        elif factory_location == "outside":
            return [FollowupAction("factory_outside_form")]
        else:
            dispatcher.utter_message(text="Unknown location. Please try again.")
            return [FollowupAction("factory_location_form")]
        
class ActionRouteAfterWarehouseSize(Action):

    # Route to small warehouse form or submit for large

    def name(self) -> Text:
        return "action_route_after_warehouse_size"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        warehouse_size = tracker.get_slot("warehouse_size")
        
        if warehouse_size == "no":
            return [FollowupAction("warehouse_small_form")]
        elif warehouse_size == "yes":
            return [FollowupAction("action_submit_fire_assessment")]
        else:
            dispatcher.utter_message(text="Unknown size. Please try again.")
            return [FollowupAction("warehouse_size_form")]


# SUBMIT FIRE ASSESSMENT
class ActionSubmitFireAssessment(Action):

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
        building_location = tracker.get_slot("building_location")
        factory_location = tracker.get_slot("factory_location")
        factory_role = tracker.get_slot("factory_role")
        warehouse_size = tracker.get_slot("warehouse_size")
        warehouse_material = tracker.get_slot("warehouse_material")
        is_critical = tracker.get_slot("is_critical")
        is_high = tracker.get_slot("is_high")
        is_rising = tracker.get_slot("is_rising")

        # Get response
        response = self._get_response(
            site_type, house_location, building_location,
            factory_location, factory_role, warehouse_size, 
            warehouse_material,
            is_critical, is_high, is_rising
        )

        # Send response
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text="🆘 Emergency Helpline: 112\n\nStay safe!")

        # Reset all slots
        return [
            SlotSet("site_type", None),
            SlotSet("house_location", None),
            SlotSet("building_location", None),
            SlotSet("factory_location", None),
            SlotSet("warehouse_size", None),
            SlotSet("warehouse_material", None),
            SlotSet("is_critical", None),
            SlotSet("is_high", None),
            SlotSet("is_rising", None)
        ]

    def _get_response(
        self, site_type, house_location, building_location,
        factory_location, factory_role, warehouse_size,
        warehouse_material,
        is_critical, is_high, is_rising
    ) -> str:

        # HOUSE
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
        
        # BUILDINGS
        elif site_type == "building":
            if building_location == "inside":
                return BUILDING_INSIDE
            else:
                return BUILDING_OUTSIDE
        
        # FACTORY
        elif site_type == "factory":
            if factory_location == "inside":
                if factory_role == "visitor":
                    return FACTORY_VISITOR
                else:
                    return FACTORY_WORKER
            else:
                risk = get_risk_level(is_critical, is_high, is_rising)
                return FACTORY_OUTSIDE.get(risk, FACTORY_OUTSIDE["low"])
        elif site_type == "warehouse":
            if warehouse_size == "large":
                return WAREHOUSE_LARGE
            else:
                risk = get_risk_level(is_critical, is_high, is_rising)
                material_responses = WAREHOUSE_SMALL.get(
                    warehouse_material,
                    WAREHOUSE_SMALL["mixed"]
                )
                return material_responses.get(risk, material_responses.get("low"))
            
        # FOREST
        elif site_type == "forest":
            risk = get_risk_level(is_critical, is_high, is_rising)
            return FOREST.get(risk, FOREST["low"])

        # DEFAULT
        else:
            return DEFAULT_RESPONSE
        
class ActionResetSlots(Action):

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
            SlotSet("building_location", None),
            SlotSet("factory_location", None),
            SlotSet("factory_role", None),
            SlotSet("warehouse_size", None),
            SlotSet("warehouse_material", None),
            SlotSet("is_critical", None),
            SlotSet("is_high", None),
            SlotSet("is_rising", None)
        ]
    
class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: dict
    ) -> list:
        
        dispatcher.utter_message(
            text="I am sorry, I didn't understand. "
                 "Type 'fire' to report a fire emergency or 'hi' to start over."
        )
        
        # Reset the conversation
        return [UserUtteranceReverted()]