from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize ChatBot
chatbot = ChatBot('MyChatBot')

# Train ChatBot using corpus data
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Interact with ChatBot
print("Type 'quit' to exit")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = chatbot.get_response(user_input)
    print("Bot:", response)
