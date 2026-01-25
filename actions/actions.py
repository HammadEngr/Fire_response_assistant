from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import UserUtteranceReverted
from datetime import datetime
# import os
import psycopg2

DATABASE_URL = "postgres://crisis_user:12&@hagYnLikj@3@db:5432/crisis_db"
# print("==DEBUG==DATABASE_URL=", DATABASE_URL)

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres_db",
        port=5432,
        dbname="crisis_db",
        user="crisis_user",
        password="12&@hagYnLikj@3"
    )
    return conn

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
    
# GET RESPONSES FROM DATABASE
def get_fire_response(response_key):
    try:
        cur = get_db_connection().cursor()
        db_query = "SELECT title, content, additional_warning FROM fire_responses WHERE response_key = %s AND is_active = true;"
        cur.execute(db_query, (response_key,))
        result = cur.fetchall()
        cur.close()

        if result:
            row = result[0]
            title, content, warning = row
            full_response = {"title": title, "content": content, "warning": warning or ""}
            return full_response
        else:
            return None
    except Exception as e:
        print(f"Database error: {e}")
        return None
    
# UPDATE USER_SUBMISSIONS FOR CRITICAL RISK
def log_critical_submission(site_type, site_location, risk_level, sender_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        upsert_query = """
            INSERT INTO user_submissions (user_id, site_type, site_location, risk_level, submission_time)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET site_type = EXCLUDED.site_type, 
                          site_location = EXCLUDED.site_location,
                          risk_level = EXCLUDED.risk_level,
                          submission_time = EXCLUDED.submission_time;
        """
        print("sender_id:", sender_id)

        cur.execute(upsert_query, (sender_id, site_type, site_location, risk_level, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error while logging submission: {e}")

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
        sender_id = tracker.sender_id
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
        response = self._get_response(sender_id,
            site_type, house_location, building_location,
            factory_location, factory_role, warehouse_size, 
            warehouse_material,
            is_critical, is_high, is_rising
        )
        default_response = get_fire_response("default_response")
        # Send response
        dispatcher.utter_message(
                    json_message={
                        "title": response["title"],
                        "sections": [{"heading":"", "content": response["content"]}],
                        "footer": response["warning"] or "",
                        "buttons": []
                    })
        dispatcher.utter_message(json_message={
                        "title": default_response["title"],
                        "sections": [{"heading":"", "content": default_response["content"]}],
                        "footer": default_response["warning"] or "",
                        "buttons": []
        })

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
        self, sender_id, site_type, house_location, building_location,
        factory_location, factory_role, warehouse_size,
        warehouse_material,
        is_critical, is_high, is_rising
    ) -> str:

        # HOUSE
        
        if site_type == "house":
            risk = get_risk_level(is_critical, is_high, is_rising)
            response_key = f"{site_type}_{house_location}_{risk}"
            house_response = get_fire_response(response_key)
            # for human escalation, insert record into user_submissions for admin to monitor
            if risk == "critical":
                log_critical_submission(
                    site_type=site_type,
                    site_location=house_location,
                    risk_level=risk,
                    sender_id=sender_id
                )
            return house_response
        
        # BUILDINGS
        elif site_type == "building":
            response_key = None
            if building_location == "inside":
                response_key = f"{site_type}_inside"
            else:
                response_key = f"{site_type}_outside"
            building_response = get_fire_response(response_key)
            return building_response
        
        # FACTORY
        elif site_type == "factory":
            response_key = None
            if factory_location == "inside":
                if factory_role == "visitor":
                    response_key = f"inside_visitor_protocol"
                else:
                    response_key = f"inside_worker_protocol"
                inside_response = get_fire_response(response_key)
                return inside_response
            else:
                risk = get_risk_level(is_critical, is_high, is_rising)
                outside_response = get_fire_response(f"outside_{site_type}_{risk}")
                if risk == "critical":
                    log_critical_submission(
                        site_type=site_type,
                        site_location=factory_location,
                        risk_level=risk,
                        sender_id=sender_id
                    )
                return outside_response

        elif site_type == "warehouse":
            if warehouse_size == "large":
                warehouse_large_response = get_fire_response("warehouse_large")
                return warehouse_large_response
            else:
                risk = get_risk_level(is_critical, is_high, is_rising)
                warehouse_small_response = get_fire_response(f"warehouse_{warehouse_material}_{risk}")
                if risk == "critical":
                    log_critical_submission(
                        site_type=site_type,
                        site_location="small warehouse",
                        risk_level=risk,
                        sender_id=sender_id
                    )
                return warehouse_small_response
            
        # FOREST
        elif site_type == "forest":
            risk = get_risk_level(is_critical, is_high, is_rising)
            forest_response = get_fire_response(f"forest_{risk}")
            if risk == "critical":
                log_critical_submission(
                    site_type=site_type,
                    site_location="forest",
                    risk_level=risk,
                    sender_id=sender_id
                )
            return forest_response

        # DEFAULT
        else:
            default_response = get_fire_response("default_response")
            return default_response
        
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