# Facebook-Message-Parser
Convert a Facebook message archive to an SQLite database for further querying.

## Usage
To run the parser, run to following command from the project root directory:

    python Message-Parser.py [Facebook_messages_archive] [alias_filename] [line_number_of_preferred_alias]
    
The alias file is simply a text file where the main user's facebook aliases are listed. One alias per line.

For example:

    Mike Green
    123456789@facebook.com
    
`[line_number_of_preferred_alias]` is an integer specifying the line number that the peferred alias to use from the list. All messages from the list will be treated as equal under this single chosen alias.

Full example:

    python Message-Parser.py "D:\Users\Mike\Desktop\fb_archive\html\messages.htm" "user_aliases.txt" 1
