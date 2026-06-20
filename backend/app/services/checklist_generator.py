def generate_transportation_checklist(is_international: bool):
    if is_international:
        return [
            {
                "title": "Learn the Bobcat Shuttle system",
                "description": "Review shuttle routes, schedules, and stops before relying on campus transportation."
            },
            {
                "title": "Review campus maps",
                "description": "Use campus maps to understand major buildings, bus stops, and walking routes."
            },
            {
                "title": "Understand ride-sharing options",
                "description": "Learn how ride-sharing services may be used as backup transportation."
            },
            {
                "title": "Review transportation safety",
                "description": "Understand basic safety practices when walking, using shuttles, or traveling at night."
            },
            {
                "title": "Review Texas driver license information",
                "description": "Understand basic Texas driver licensing information if you plan to drive."
            }
        ]

    return [
        {
            "title": "Review parking permit information",
            "description": "Understand parking permit options and campus parking rules."
        },
        {
            "title": "Review campus maps",
            "description": "Use campus maps to identify parking areas, buildings, and transportation routes."
        },
        {
            "title": "Review transportation services",
            "description": "Review available Texas State transportation services."
        }
    ]