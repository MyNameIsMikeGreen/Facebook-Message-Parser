DEFAULT_MESSAGE_TABLE_DETAILS = {
        "name": "Messages",
        "columns": [
            {
                "name": "Message_ID",
                "type": "integer",
                "attributes": ["primary", "key", "autoincrement"]
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

DEFAULT_ACTOR_TABLE_DETAILS = {
    "name": "Actors",
    "columns": [
        {
            "name": "Actor_ID",
            "type": "integer",
            "attributes": ["primary", "key", "autoincrement"]
        },
        {
            "name": "Actor_Name",
            "type": "text",
            "unique": True
        }
    ]
}

DEFAULT_CONVERSATION_TABLE_DETAILS = {
    "name": "Conversations",
    "columns": [
        {
            "name": "Conversation_ID",
            "type": "integer",
            "attributes": ["primary", "key", "autoincrement"]
        },
        {
            "name": "Conversation_Name",
            "type": "text"
        }
    ]
}

DEFAULT_TABLE_DETAILS_LIST = [DEFAULT_MESSAGE_TABLE_DETAILS, DEFAULT_ACTOR_TABLE_DETAILS,
                              DEFAULT_CONVERSATION_TABLE_DETAILS]
