import React, {useEffect, useState} from 'react';
import { Card, CardContent } from "./components/ui/Card";
import { Input } from "./components/ui/Input";
import { Button } from "./components/ui/Button";
import { v4 as uuidv4 } from 'uuid';

const LOCAL_STORAGE_KEY = 'chatbot_conversations';

const ChatbotPage = () => {
    const [conversations, setConversations] = useState([]);
    const [currentId, setCurrentId] = useState(null);
    const [input, setInput] = useState('');

    useEffect(() => {
        const stored = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || [];
        setConversations(stored);

        if (stored.length > 0) setCurrentId(stored[0].id);
        else handleNewConversation();
    }, []);

    useEffect(() => {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(conversations));
    }, [conversations]);

    const currentConversation = conversations.find(c => c.id === currentId);

    const handleSend = async () => {
        if (!input.trim() || !currentConversation) return;

        const userMsg = { sender: 'user', text: input };

        // Show "thinking..." placeholder
        const loadingBotMsg = { sender: 'bot', text: 'Generating recipe...' };

        // Add messages to UI first
        const updated = conversations.map((c) => {
            if (c.id === currentId) {
                return {
                    ...c,
                    messages: [...c.messages, userMsg, loadingBotMsg],
                };
            }
            return c;
        });

        setConversations(updated);
        setInput('');

        try {
            const response = await fetch('http://localhost:5000/generate-recipe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ingredients: input }),
            });

            const data = await response.json();
            const message = `Here's the recipe I found for you!` + "\n🌟 Ingredients 🌟"+
                `${data.ingredients.join(',')}` +
                "\n🍳 Instructions 🍳\n" +
                `${data.instructions.join(', ')}`;

            const finalBotMsg = {
                sender: 'bot',
                text: message || 'No recipe returned.',
            };

            const finalConversations = updated.map((c) => {
                if (c.id === currentId) {
                    const withoutTemp = c.messages.slice(0, -1); // Remove "thinking..."
                    return {
                        ...c,
                        messages: [...withoutTemp, finalBotMsg],
                    };
                }
                return c;
            });

            setConversations(finalConversations);
        } catch (error) {
            console.error('Error generating recipe:', error);

            const errorBotMsg = {
                sender: 'bot',
                text: 'Oops! Something went wrong while generating the recipe. Please try again.',
            };

            const erroredConversations = updated.map((c) => {
                if (c.id === currentId) {
                    const withoutTemp = c.messages.slice(0, -1);
                    return {
                        ...c,
                        messages: [...withoutTemp, errorBotMsg],
                    };
                }
                return c;
            });

            setConversations(erroredConversations);
        }
    };



    const handleKeyDown = (e) => {
        if (e.key === 'Enter') handleSend();
    };

    const handleNewConversation = () => {
        const newId = uuidv4();
        const newConvo = {
            id: newId,
            title: `Recipe ${conversations.length + 1}`,
            messages: [
                { sender: 'bot', text: "Are you hungry? Let's find a recipe for you! What's in your kitchen today?" }
            ]
        };

        setConversations([newConvo, ...conversations]);
        setCurrentId(newId);
        setInput('');
    };

    const switchConversation = (id) => {
        setCurrentId(id);
        setInput('');
    };

    return (
        <div className="min-h-screen flex bg-slate-900 text-white">
            <div className="w-64 bg-slate-800 p-4 flex flex-col">
                <h2 className="text-xl font-bold mb-4">iCook</h2>
                <Button onClick={handleNewConversation} className="mb-4 w-full">
                    Search for a new recipe
                </Button>
                <div className="flex-1 overflow-y-auto space-y-2">
                    {conversations.map((conv) => (
                        <button
                            key={conv.id}
                            onClick={() => switchConversation(conv.id)}
                            className={`text-left p-2 rounded-lg w-full ${
                                conv.id === currentId
                                    ? 'bg-blue-600'
                                    : 'bg-slate-700 hover:bg-slate-600'
                            }`}
                        >
                            {conv.title}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex-1 p-6 flex flex-col">
                <Card className="flex-1 flex flex-col">
                    <CardContent className="flex-1 flex flex-col overflow-hidden">
                        <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                            {currentConversation?.messages.map((msg, i) => (
                                <div
                                    key={i}
                                    className={`max-w-xs p-3 rounded-xl ${
                                        msg.sender === 'user'
                                            ? 'ml-auto bg-blue-600 text-white'
                                            : 'mr-auto bg-gray-200 text-gray-800'
                                    }`}
                                >
                                    {msg.text}
                                </div>
                            ))}
                        </div>

                        <div className="flex gap-2 items-center mt-4">
                            <Input
                                className="flex-1 text-black"
                                placeholder="Type your message..."
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                            />
                            <Button onClick={handleSend}>Send</Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default ChatbotPage;
