import React, { useState } from 'react';
import { X, Star, MessageSquare } from 'lucide-react';
import { api } from '../api/client';

const FeedbackModal = ({ isOpen, onClose, sessionId, messageId }) => {
    const [rating, setRating] = useState(0);
    const [comment, setComment] = useState('');
    const [loading, setLoading] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (rating === 0) return;

        setLoading(true);
        try {
            await api.submitFeedback(sessionId, messageId, rating, comment);
            setSubmitted(true);
            setTimeout(() => {
                onClose();
                setSubmitted(false);
                setRating(0);
                setComment('');
            }, 2000);
        } catch (error) {
            console.error("Feedback failed", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-96 shadow-xl relative">
                <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
                    <X size={20} />
                </button>

                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <MessageSquare className="text-blue-500" /> Rate Response
                </h2>

                {submitted ? (
                    <div className="text-center py-4 bg-green-50 rounded text-green-700">
                        Thanks for your feedback!
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="flex justify-center space-x-2">
                            {[1, 2, 3, 4, 5].map((star) => (
                                <button
                                    key={star}
                                    type="button"
                                    onClick={() => setRating(star)}
                                    className={`p-1 transition-colors ${rating >= star ? 'text-yellow-400' : 'text-gray-300'}`}
                                >
                                    <Star fill={rating >= star ? "currentColor" : "none"} size={32} />
                                </button>
                            ))}
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Comment (Optional)</label>
                            <textarea
                                value={comment}
                                onChange={(e) => setComment(e.target.value)}
                                className="w-full border rounded p-2 h-24 resize-none"
                                placeholder="What did you like or dislike?"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading || rating === 0}
                            className="w-full bg-blue-600 text-white py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
                        >
                            {loading ? 'Submitting...' : 'Submit Feedback'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};

export default FeedbackModal;
