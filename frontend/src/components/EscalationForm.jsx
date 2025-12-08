import React, { useState } from 'react';
import { X, AlertCircle } from 'lucide-react';
import { api } from '../api/client';

const EscalationForm = ({ isOpen, onClose, sessionId, messageId }) => {
    const [reason, setReason] = useState('billing');
    const [severity, setSeverity] = useState('medium');
    const [loading, setLoading] = useState(false);
    const [ticket, setTicket] = useState(null);

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.escalate(sessionId, messageId, reason, severity);
            setTicket(res.data);
        } catch (error) {
            console.error("Escalation failed", error);
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
                    <AlertCircle className="text-red-500" /> Escalate Issue
                </h2>

                {ticket ? (
                    <div className="bg-green-50 p-4 rounded text-center">
                        <h3 className="text-green-800 font-bold mb-2">Ticket Created!</h3>
                        <p className="text-sm">Ref: <strong>{ticket.ticket_ref}</strong></p>
                        <p className="text-sm">ETA: {ticket.estimated_response_time}</p>
                        <button onClick={onClose} className="mt-4 bg-gray-900 text-white px-4 py-2 rounded w-full">
                            Close
                        </button>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Reason</label>
                            <select
                                value={reason}
                                onChange={(e) => setReason(e.target.value)}
                                className="w-full border rounded p-2"
                            >
                                <option value="billing">Billing Issue</option>
                                <option value="technical">Technical Support</option>
                                <option value="account">Account Access</option>
                                <option value="other">Other</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Severity</label>
                            <div className="flex gap-4">
                                {['low', 'medium', 'high'].map(sev => (
                                    <label key={sev} className="flex items-center gap-1 cursor-pointer">
                                        <input
                                            type="radio"
                                            name="severity"
                                            value={sev}
                                            checked={severity === sev}
                                            onChange={(e) => setSeverity(e.target.value)}
                                        />
                                        <span className="capitalize">{sev}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-red-600 text-white py-2 rounded font-medium hover:bg-red-700 disabled:opacity-50"
                        >
                            {loading ? 'Processing...' : 'Create Ticket'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};

export default EscalationForm;
