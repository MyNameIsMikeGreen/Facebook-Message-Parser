MESSAGE_TABLE_DETAILS = {
        "name": "Messages",
        "columns": [
            {
                "name": "Message_ID",
                "type": "text",
                "attributes": ["primary", "key"]
            },
            {
                "name": "Actor_ID",
                "type": "integer"
            },
            {
                "name": "Conversation_ID",
                "type": "integer"
            },
            {
                "name": "Timestamp",
                "type": "integer"
            },
            {
                "name": "Content",
                "type": "text"
            }
        ]
    }

ACTOR_TABLE_DETAILS = {
    "name": "Actors",
    "columns": [
        {
            "name": "Actor_ID",
            "type": "text",
            "attributes": ["primary", "key"]
        },
        {
            "name": "Actor_Name",
            "type": "text",
            "unique": True
        }
    ]
}

CONVERSATION_TABLE_DETAILS = {
    "name": "Conversations",
    "columns": [
        {
            "name": "Conversation_ID",
            "type": "text",
            "attributes": ["primary", "key"]
        },
        {
            "name": "Conversation_Name",
            "type": "text"
        }
    ]
}

TABLE_DETAILS_LIST = [MESSAGE_TABLE_DETAILS, ACTOR_TABLE_DETAILS, CONVERSATION_TABLE_DETAILS]
