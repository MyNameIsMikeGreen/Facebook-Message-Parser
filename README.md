# Facebook-Message-Parser
Convert a Facebook message archive to an SQLite database for further querying.

## Running the Script
To run the parser, run to following command from the project root directory:

    python Message-Parser.py [Facebook_messages_archive] [alias_filename] [line_number_of_preferred_alias]
    
The alias file is simply a text file where the main user's facebook aliases are listed. One alias per line.

For example:

    Mike Green
    123456789@facebook.com
    
`[line_number_of_preferred_alias]` is an integer specifying the line number that the peferred alias to use from the list. All messages from the list will be treated as equal under this single chosen alias.

Full example:

    python Message-Parser.py "D:\Users\Mike\Desktop\fb_archive\html\messages.htm" "user_aliases.txt" 1
    
## Running Queries on the Database
The database is set up as a simple flat file table named `Messages`.

| Field Name        | Data Type                |
| ------------------|:------------------------:|
| Message_ID        | Auto-incremented INTEGER |
| Message_Text      | TEXT                     |
| Message_DateTime  | TEXT                     |
| Message_Sender    | TEXT                     |
| Message_Receiver  | TEXT                     |

Each tuple represents the properties of a single message.

## Future Developments
* Add support for group chats
* Increased performance
* Interface for incorporation into other applications
* Add support for strings with single-quotes
* Improve database schema from flat file
