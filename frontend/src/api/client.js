import axios from 'axios';

const API_URL = 'http://localhost:8000';

const client = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    // Session
    createSession: (userId) => client.post('/session', { user_id: userId }),
    getSessionHistory: (sessionId) => client.get(`/session/${sessionId}/history`),

    // Chat
    sendMessage: (sessionId, message, stream = false) =>
        client.post('/chat', { session_id: sessionId, message, stream }),

    // Feedback
    submitFeedback: (sessionId, messageId, rating, comment) =>
        client.post('/feedback', {
            session_id: sessionId,
            message_id: messageId,
            rating,
            comment
        }),

    // Escalation
    escalate: (sessionId, messageId, reason, severity) =>
        client.post('/escalate', {
            session_id: sessionId,
            message_id: messageId,
            reason,
            severity
        })
};
