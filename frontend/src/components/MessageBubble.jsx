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
                <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                    <Bot className="h-6 w-6 text-blue-600 dark:text-blue-300" />
                </div>
            )}

            <div className={clsx(
                "relative rounded-lg px-4 py-2 text-sm shadow-sm transition-colors duration-300",
                isAssistant
                    ? "bg-white border border-gray-100 text-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100"
                    : "bg-blue-600 text-white"
            )}>
                <div className={clsx("prose prose-sm max-w-none", isAssistant && "dark:prose-invert")}>
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>

                {/* Footer actions for Assistant */}
                {isAssistant && message.message_id && (
                    <div className="mt-2 flex items-center space-x-4 border-t pt-2 border-gray-100 dark:border-gray-700">
                        {/* Confidence Debug */}
                        {message.confidence && (
                            <span className="text-xs text-gray-400 dark:text-gray-500">
                                Confidence: {Math.round(message.confidence * 100)}%
                            </span>
                        )}

                        <button
                            onClick={handleRating}
                            className={clsx("p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors", rated ? "text-green-500" : "text-gray-400 dark:text-gray-500")}
                            title="Rate Helpful"
                        >
                            <ThumbsUp size={14} />
                        </button>

                        <button
                            onClick={() => onEscalate(message.message_id)}
                            className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-400 dark:text-gray-500 hover:text-red-500"
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
