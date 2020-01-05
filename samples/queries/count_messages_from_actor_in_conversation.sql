SELECT COUNT(Messages.Content)
FROM Messages
INNER JOIN Actors ON Messages.Actor_ID=Actors.Actor_ID
INNER JOIN Conversations ON Conversations.Conversation_ID=Messages.Conversation_ID
WHERE Conversations.Conversation_ID='aaaaa-bbbbb-ccccc-ddddd'
	AND Actors.Actor_Name='actor123';
