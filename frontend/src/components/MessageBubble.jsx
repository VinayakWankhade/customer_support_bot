import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Bot, User, ThumbsUp, AlertTriangle } from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api/client';

const MessageBubble = ({ message, sessionId, onFeedback, onEscalate }) => {
    const isAssistant = message.role === 'assistant';
    const [rated, setRated] = useState(false);

    const handleRating = async () => {
        if (rated) return;
        try {
            await api.submitFeedback(sessionId, message.message_id, 5, 'Liked via UI');
            setRated(true);
            onFeedback && onFeedback();
        } catch (e) {
            console.error("Feedback failed", e);
        }
    };

    return (
        <div className={clsx(
            "flex w-full mt-4 space-x-3 max-w-3xl mx-auto",
            isAssistant ? "justify-start" : "justify-end"
        )}>
            {isAssistant && (
                <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <Bot className="h-6 w-6 text-blue-600" />
                </div>
            )}

            <div className={clsx(
                "relative rounded-lg px-4 py-2 text-sm shadow-sm",
                isAssistant ? "bg-white border border-gray-100 text-gray-900" : "bg-blue-600 text-white"
            )}>
                <div className="prose prose-sm max-w-none">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>

                {/* Footer actions for Assistant */}
                {isAssistant && message.message_id && (
                    <div className="mt-2 flex items-center space-x-4 border-t pt-2 border-gray-100">
                        {/* Confidence Debug */}
                        {message.confidence && (
                            <span className="text-xs text-gray-400">
                                Confidence: {Math.round(message.confidence * 100)}%
                            </span>
                        )}

                        <button
                            onClick={handleRating}
                            className={clsx("p-1 rounded hover:bg-gray-100", rated ? "text-green-500" : "text-gray-400")}
                            title="Rate Helpful"
                        >
                            <ThumbsUp size={14} />
                        </button>

                        <button
                            onClick={() => onEscalate(message.message_id)}
                            className="p-1 rounded hover:bg-gray-100 text-gray-400 hover:text-red-500"
                            title="Escalate Issue"
                        >
                            <AlertTriangle size={14} />
                        </button>
                    </div>
                )}
            </div>

            {!isAssistant && (
                <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                    <User className="h-6 w-6 text-gray-500" />
                </div>
            )}
        </div>
    );
};

export default MessageBubble;
