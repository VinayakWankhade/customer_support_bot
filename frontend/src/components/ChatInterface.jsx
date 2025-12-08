import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import { api } from '../api/client';
import MessageBubble from './MessageBubble';
import EscalationForm from './EscalationForm';

const ChatInterface = () => {
    const [sessionId, setSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [escalationData, setEscalationData] = useState({ isOpen: false, messageId: null });
    const messagesEndRef = useRef(null);

    // Initialize Session
    useEffect(() => {
        const initSession = async () => {
            try {
                // Check local storage or create new
                const savedSession = localStorage.getItem('chat_session_id');
                if (savedSession) {
                    setSessionId(savedSession);
                    // Restore history
                    try {
                        const res = await api.getSessionHistory(savedSession);
                        setMessages(res.data.messages || []);
                    } catch (e) {
                        // If not found, create new
                        createNewSession();
                    }
                } else {
                    createNewSession();
                }
            } catch (error) {
                console.error("Failed to init session", error);
            }
        };
        initSession();
    }, []);

    const createNewSession = async () => {
        try {
            const res = await api.createSession();
            const newId = res.data.session_id;
            setSessionId(newId);
            localStorage.setItem('chat_session_id', newId);
            setMessages([]);
        } catch (e) {
            console.error("Create session failed", e);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading || !sessionId) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            // Optimistic update for assistant? No, wait for response because we need metadata like confidence/sources
            // For streaming, we would need to handle chunks. For now implementing non-streaming UI based on current backend test
            const res = await api.sendMessage(sessionId, userMsg.content);

            // Adapt response to message format
            const assistantMsg = {
                role: 'assistant',
                content: res.data.answer_text,
                confidence: res.data.confidence,
                message_id: res.data.message_id || 'temp-id', // Backend should return message_id in chat response schema!
                // If chat response doesn't return message_id, we might miss it for feedback.
                // Let's assume Updated Schema returns it, else we rely on history/reload.
                // Actually, previous artifact walkthrough showed message_id in ChatResponse.
            };

            setMessages(prev => [...prev, assistantMsg]);
        } catch (error) {
            console.error("Chat error", error);
            setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ Error: Could not reach the agent.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center z-10">
                <h1 className="text-xl font-bold text-gray-800">Support Bot</h1>
                <div className="text-sm text-gray-500 font-mono">
                    Session: {sessionId?.slice(0, 8)}...
                </div>
            </header>

            {/* Messages */}
            <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
                <div className="max-w-3xl mx-auto space-y-6">
                    {messages.length === 0 && (
                        <div className="text-center text-gray-400 mt-20">
                            <p>👋 How can I help you today?</p>
                        </div>
                    )}

                    {messages.map((msg, idx) => (
                        <MessageBubble
                            key={idx}
                            message={msg}
                            sessionId={sessionId}
                            onEscalate={(msgId) => setEscalationData({ isOpen: true, messageId: msgId })}
                        />
                    ))}

                    {loading && (
                        <div className="flex justify-start w-full max-w-3xl mx-auto mt-4">
                            <div className="bg-white border p-3 rounded-lg shadow-sm">
                                <span className="animate-pulse">Typing...</span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </main>

            {/* Input */}
            <footer className="bg-white border-t p-4">
                <form onSubmit={handleSend} className="max-w-3xl mx-auto relative flex items-center">
                    <input
                        type="text"
                        className="w-full border border-gray-300 rounded-full py-3 px-5 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                        placeholder="Type your message..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="absolute right-2 p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </footer>

            <EscalationForm
                isOpen={escalationData.isOpen}
                onClose={() => setEscalationData({ ...escalationData, isOpen: false })}
                sessionId={sessionId}
                messageId={escalationData.messageId}
            />
        </div>
    );
};

export default ChatInterface;
