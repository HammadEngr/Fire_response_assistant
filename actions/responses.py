# FIRE EMERGENCY RESPONSE CONTENT
# ============================================================

# HOUSE RESPONSES
HOUSE_CRITICAL = """🚨 CRITICAL - IMMEDIATE RESCUE PLAN

1. Everyone including pets must leave IMMEDIATELY
2. Call 112 once outside at safe distance
3. If clothes catch fire: STOP, DROP, ROLL
4. Do NOT attempt to extinguish
5. Stay LOW to avoid smoke
6. If trapped:
   • Move to room with window
   • Seal door gaps with wet cloth
   • Signal for help
7. Do NOT reopen closed doors
8. Do NOT touch electrical wires"""

HOUSE_HIGH = """🟠 HIGH RISK

• Do NOT attempt firefighting
• Evacuate immediately
• Stay low to avoid smoke
• Close doors behind you to contain fire
• Call 112
• Warn others nearby"""

HOUSE_RISING = """🟡 RISING RISK

• Prepare to evacuate
• Keep exits clear
• Turn off appliances if safely reachable
• Alert everyone in house

If situation worsens, evacuate immediately."""

HOUSE_LOW = """🟢 LOW RISK - Early Stage

• Stay calm, keep exit behind you
• Identify fire source
• If small and contained, use appropriate extinguisher
• Never use water on oil/electrical fire

If fire doesn't go out in seconds, evacuate."""

HOUSE_KITCHEN = {
    "critical": HOUSE_CRITICAL,
    "high": HOUSE_HIGH + "\n\n⚠️ KITCHEN: Synthetic materials create toxic smoke.",
    "rising": HOUSE_RISING + "\n\n⚠️ If gas smell: Evacuate immediately, no switches, no flames.",
    "low": HOUSE_LOW + "\n\n⚠️ KITCHEN: Never use water on oil fires. Use fire blanket or Class K extinguisher."
}

HOUSE_ELECTRICAL = {
    "critical": HOUSE_CRITICAL + "\n\n⚠️ ELECTRICAL: Keep hands/feet dry. Use rubber sole footwear. Do NOT touch walls.",
    "high": HOUSE_HIGH + "\n\n⚠️ ELECTRICAL: Smoke is toxic. Re-energization risk even after flames stop.",
    "rising": HOUSE_RISING + "\n\n⚠️ ELECTRICAL: Isolate power if safe. Never use water. Class C extinguisher only.",
    "low": HOUSE_LOW + "\n\n⚠️ ELECTRICAL: Isolate power at main breaker. Water extinguishers prohibited."
}

HOUSE_BEDROOM = {
    "critical": HOUSE_CRITICAL,
    "high": HOUSE_HIGH + "\n\n⚠️ BEDROOM: Foam and synthetic materials release lethal gases.",
    "rising": HOUSE_RISING + "\n\n⚠️ BEDROOM: Close doors to slow spread. Upholstery smoke is toxic.",
    "low": HOUSE_LOW + "\n\n⚠️ BEDROOM: Switch off heating appliances. Keep fire away from soft furnishings."
}

HOUSE_GARAGE = {
    "critical": HOUSE_CRITICAL + "\n\n⚠️ GARAGE: Extreme hazard! Aerosols, batteries, chemicals may explode. Establish exclusion zone.",
    "high": HOUSE_HIGH + "\n\n⚠️ GARAGE: Most hazardous area in house. Close door between garage and house. Do NOT attempt firefighting.",
    "rising": HOUSE_RISING + "\n\n⚠️ GARAGE: Stop all activities. Isolate power if safe. Lithium batteries may rupture.",
    "low": HOUSE_LOW + "\n\n⚠️ GARAGE HAZARDS: Paints, solvents, aerosols, batteries, poor ventilation. Keep safe distance."
}

HOUSE_GAS = {
    "critical": """🚨 GAS AREA - EXTREME DANGER

⚠️ GAS + FIRE = EXPLOSION RISK

1. EVACUATE IMMEDIATELY
2. Do NOT operate electrical switches
3. Do NOT use mobile phone near area
4. Move UPWIND to safe distance
5. Call 112 from safe location
6. Warn neighbors

Do NOT attempt to shut off gas if fire is present.""",
    "high": """🟠 GAS AREA - TREAT AS CRITICAL

• Evacuate NOW
• No electrical switches
• No ignition sources
• Move upwind
• Call 112 from safe distance""",
    "rising": """🟡 GAS SMELL DETECTED - CRITICAL WARNING

⚠️ Gas leak is critical even without fire

• Evacuate immediately
• No electrical switches
• No flames
• Open windows only if on exit path
• Shut off gas ONLY if instantly accessible
• Call 112 from outside""",
    "low": """🟡 GAS AREA - CAUTION

Even at low risk, gas areas require caution:
• No open flames
• Know gas shutoff location
• Check connections regularly

If you smell gas at any point - evacuate immediately."""
}

HOUSE_OTHER = {
    "critical": HOUSE_CRITICAL,
    "high": HOUSE_HIGH,
    "rising": HOUSE_RISING,
    "low": HOUSE_LOW
}

# BUILDING RESPONSES
# ============================================================

BUILDING_INSIDE = """🏢 BUILDING FIRE - INSIDE

Follow Building Safety Protocols:

1. Do NOT panic
2. Listen to fire alarm and PA announcements
3. Follow instructions from fire wardens / security
4. Use stairs only - NEVER elevators
5. Proceed to designated assembly points
6. Do NOT push or run

Stampede Prevention:
• Move quickly but calmly
• Follow flow of people
• Keep arms raised to protect chest
• Move towards walls if crowd is dense
• If fell: curl into ball, protect head

Do NOT:
• Investigate the fire
• Return for belongings
• Re-enter the building
• Spread unverified information"""

BUILDING_OUTSIDE = """🏢 BUILDING FIRE - OUTSIDE

Your Actions:

1. Call 112 immediately
2. Report:
   • Building location/address
   • What you see (smoke, flames, floor)
   • Any people visible at windows
3. Stay at safe distance
4. Do NOT enter the building
5. Direct fire services when they arrive
6. Help keep area clear for emergency vehicles

Do NOT:
• Attempt rescue yourself
• Block emergency access
• Spread panic"""

# FACTORY RESPONSES
# ============================================================

FACTORY_WORKER = """🏭 FACTORY FIRE - WORKER PROTOCOL

Immediate Actions:
1. Raise alarm - activate nearest call point
2. Stop work immediately
3. Alert nearby colleagues

Evacuation:
• Follow site emergency procedures
• Use designated escape routes
• Do NOT use elevators
• Proceed to muster/assembly point
• Move calmly, avoid running

Firefighting (Only if trained):
• Fire is small and controllable
• Correct extinguisher available
• Clear escape route behind you
• Stop if smoke increases

Critical Rules:
• Do NOT attempt rescue beyond training
• Do NOT collect belongings
• Do NOT re-enter until authorized
• Be aware of: chemicals, pressurized systems, electrical equipment

At Assembly Point:
• Report to supervisor/fire warden
• Participate in roll call
• Report missing persons"""

FACTORY_VISITOR = """🏭 FACTORY FIRE - VISITOR PROTOCOL

Immediate Actions:
1. Alert nearest staff member
2. Do NOT investigate or fight fire
3. Follow staff instructions

Evacuation:
• Evacuate when instructed
• Follow marked exit signs
• Use stairs only
• Stay with your escort/guide

Safety Rules:
• Do NOT touch equipment or controls
• Do NOT enter restricted areas
• Do NOT separate from group

At Assembly Point:
• Go to visitor assembly area
• Stay until given clearance
• Inform staff of missing companions"""

FACTORY_OUTSIDE = {
    "critical": """🏭 FACTORY FIRE - OUTSIDE (CRITICAL)

⚠️ You are very close to danger

1. Move AWAY immediately (upwind if possible)
2. Do NOT enter the facility
3. Call 112 immediately
4. Warn people nearby

Report to 112:
• Factory location
• What you see (smoke, flames, area)
• Any explosions heard

Stay at safe distance until emergency services arrive.""",
    "high": """🏭 FACTORY FIRE - OUTSIDE (HIGH RISK)

Fire is visible and active:

1. Call 112 immediately
2. Report location and what you see
3. Stay at safe distance
4. Move further if wind shifts

Do NOT:
• Enter the facility
• Approach for photos
• Block access roads""",
    "rising": """🏭 FACTORY FIRE - OUTSIDE (RISING)

You see early signs:

1. Call 112 to report
2. Inform security if present
3. Keep observing from safe distance
4. Be ready to move further

Monitor wind direction - smoke may spread.""",
    "low": """🏭 FACTORY FIRE - OUTSIDE (LOW)

You see distant signs:

1. Call 112 to report:
   • Location
   • What you observe
2. Stay at distance
3. Do NOT approach

Factory fires can escalate quickly. Stay alert."""
}

# WAREHOUSE RESPONSES
# ============================================================

WAREHOUSE_LARGE = """🏬 LARGE WAREHOUSE - SAFETY PROTOCOL

This facility has established safety procedures.

Follow Your Site's Emergency Plan:
1. Raise alarm using nearest call point
2. Stop all operations (forklifts, conveyors)
3. Alert nearby workers
4. Follow site evacuation procedures
5. Proceed to designated muster point

Warehouse Hazards:
• High-rack storage = rapid spread
• Falling goods risk
• Forklifts and charging stations
• Combustible packaging

Safety Rules:
• Do NOT enter high-rack aisles during fire
• Do NOT move pallets or stock
• Close fire doors if instructed

At Assembly Point:
• Report to supervisor/fire warden
• Participate in roll call
• Report missing persons

Your safety team is trained for this. Follow their lead."""

WAREHOUSE_SMALL = {
    "garments": {
        "critical": """🚨 GARMENTS WAREHOUSE - CRITICAL

⚠️ Toxic smoke hazard!

1. Evacuate IMMEDIATELY
2. Stay low, cover nose/mouth
3. Move upwind if outside
4. Call 112

Do NOT attempt firefighting.
Synthetic fibers generate lethal smoke.""",
        "high": "🟠 GARMENTS - HIGH RISK\n\nEvacuate now. Toxic smoke risk. Do NOT use water on burning synthetics.",
        "rising": "🟡 GARMENTS - RISING\n\nPrepare to evacuate. Keep exits clear. Monitor smoke.",
        "low": "🟢 GARMENTS - LOW\n\nStay alert. Control ignition sources. Maintain evacuation readiness."
    },
    "electrical": {
        "critical": """🚨 ELECTRICAL WAREHOUSE - CRITICAL

1. Evacuate IMMEDIATELY
2. Do NOT touch equipment
3. Do NOT use water
4. Call 112

Live-current and re-ignition risks.""",
        "high": "🟠 ELECTRICAL - HIGH RISK\n\nEvacuate now. Isolate main power ONLY if instantly accessible. NO water/foam.",
        "rising": "🟡 ELECTRICAL - RISING\n\nKeep safe distance. Use CO2 or Class C extinguisher only if trained.",
        "low": "🟢 ELECTRICAL - LOW\n\nIsolate faulty equipment. Ventilate. Arrange inspection before re-energizing."
    },
    "mechanical": {
        "critical": """🚨 MECHANICAL WAREHOUSE - CRITICAL

1. Evacuate IMMEDIATELY
2. Move upwind
3. Call 112

Oil, fuel, battery explosion risks.""",
        "high": "🟠 MECHANICAL - HIGH RISK\n\nEvacuate. Avoid stored oils/batteries. Use Dry Powder (ABC) only if trained.",
        "rising": "🟡 MECHANICAL - RISING\n\nRemove ignition sources. ABC extinguisher if trained. NO water on oils.",
        "low": "🟢 MECHANICAL - LOW\n\nSwitch off machinery. Contain leaks if trained."
    },
    "wood": {
        "critical": """🚨 WOOD/PAPER WAREHOUSE - CRITICAL

Rapid-spread fire environment!

1. Evacuate IMMEDIATELY
2. Stay low, cover nose/mouth
3. Move upwind
4. Call 112""",
        "high": "🟠 WOOD/PAPER - HIGH RISK\n\nEvacuate. Keep clear of stacked materials (collapse risk). Water/Foam if trained.",
        "rising": "🟡 WOOD/PAPER - RISING\n\nMaintain escape route. Remove ignition sources. Water/Foam/ABC if trained.",
        "low": "🟢 WOOD/PAPER - LOW\n\nSeparate smoldering materials. Improve housekeeping and spacing."
    },
    "ceramics": {
        "critical": """🚨 CERAMICS/GLASS WAREHOUSE - CRITICAL

Shatter and collapse risks!

1. Evacuate IMMEDIATELY
2. Protect head/face from falling materials
3. Move away from racks
4. Call 112""",
        "high": "🟠 CERAMICS/GLASS - HIGH RISK\n\nEvacuate. Keep clear of glass stacks. Avoid vibration/impact.",
        "rising": "🟡 CERAMICS/GLASS - RISING\n\nControl access. Water/Foam/ABC if trained.",
        "low": "🟢 CERAMICS/GLASS - LOW\n\nRestrict movement near stacked goods. Switch off faulty equipment."
    },
    "rubber": {
        "critical": """🚨 RUBBER/PLASTICS WAREHOUSE - CRITICAL

⚠️ EXTREME RISK - Intense heat, toxic smoke!

1. Evacuate IMMEDIATELY
2. Stay low, cover nose/mouth
3. Move upwind
4. Establish WIDE exclusion zone
5. Call 112

Do NOT re-enter under any circumstances.""",
        "high": "🟠 RUBBER/PLASTICS - HIGH RISK\n\nEvacuate IMMEDIATELY. Close doors to limit oxygen. NO water on large fires.",
        "rising": "🟡 RUBBER/PLASTICS - RISING\n\nPrepare to evacuate. Foam or ABC if trained. Water not effective.",
        "low": "🟢 RUBBER/PLASTICS - LOW\n\nSwitch off machinery. Increase ventilation. Keep Foam/ABC on standby."
    },
    "chemicals": {
        "critical": """🚨 CHEMICALS WAREHOUSE - CRITICAL

⚠️ AUTHORITY-ONLY EMERGENCY

1. Evacuate IMMEDIATELY
2. Move UPWIND
3. Cover nose/mouth
4. Avoid low areas
5. Establish WIDE exclusion zone
6. Call 112 - Request HAZMAT team

ABSOLUTE RULES:
• Do NOT identify chemicals yourself
• Do NOT mix substances
• Do NOT use water or foam
• Do NOT use standard extinguishers
• ALWAYS escalate to specialists""",
        "high": "🚨 CHEMICALS - TREAT AS CRITICAL\n\nEvacuate. Report 'chemical warehouse' to 112. Request HAZMAT.",
        "rising": "🟠 CHEMICALS - RISING\n\nKeep distance. No contact with substances. Call 112 for assessment.",
        "low": "🟡 CHEMICALS - CAUTION\n\nEven at low risk, do NOT attempt firefighting. Notify management. Call specialists."
    },
    "mixed": {
        "critical": """🚨 WAREHOUSE - CRITICAL

Unknown materials = unknown risks.

1. Evacuate IMMEDIATELY
2. Stay low, cover nose/mouth
3. Move upwind
4. Call 112
5. Report materials are unknown/mixed""",
        "high": "🟠 WAREHOUSE - HIGH RISK\n\nEvacuate. Do not attempt firefighting with unknown materials.",
        "rising": "🟡 WAREHOUSE - RISING\n\nPrepare to evacuate. If you know material, use appropriate extinguisher.",
        "low": "🟢 WAREHOUSE - LOW\n\nTry to identify materials if safe. Report to supervisor. Maintain readiness."
    }
}

# FOREST RESPONSES
# ============================================================

FOREST = {
    "critical": """🌲 WILDFIRE - CRITICAL

⚠️ IMMEDIATE ESCAPE REQUIRED

1. Leave area IMMEDIATELY
2. Move UPWIND and DOWNHILL if possible
3. Avoid narrow valleys and dense vegetation
4. Cover nose/mouth

If trapped:
• Find clearing or water body
• If in vehicle: close windows/vents
• Last resort: find depression, cover with soil

Call 112 with:
• Your location
• Fire direction
• Escape route status""",
    "high": """🟠 WILDFIRE - HIGH RISK

Fire is visible and active:

1. Move away NOW while routes clear
2. Do NOT wait to observe
3. Call 112
4. Follow evacuation orders

If wind shifts or fire accelerates - treat as CRITICAL.""",
    "rising": """🟡 WILDFIRE - RISING

Early signs detected:

1. Prepare to leave
2. Report to authorities
3. Watch wind direction
4. Keep escape routes clear

Do NOT approach the fire.""",
    "low": """🟢 WILDFIRE - LOW

Distant signs observed:

1. Report location to fire services
2. Maintain safe distance
3. Monitor official alerts
4. Do NOT approach for viewing

Forest fires change rapidly. Stay aware."""
}

# DEFAULT RESPONSE
# ============================================================

DEFAULT_RESPONSE = """⚠️ Fire Emergency

1. Call 112 immediately
2. Evacuate the area
3. Move to safe distance
4. Wait for emergency services"""