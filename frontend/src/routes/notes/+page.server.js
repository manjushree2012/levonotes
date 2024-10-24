import { error } from '@sveltejs/kit';
import { API_BASE_URL } from '$env/static/private';

/** @type {import('./$types').PageServerLoad} */
export const load = async ({ fetch }) => {
    try {
        const response = await fetch(`${API_BASE_URL}/notes`);
        if (!response.ok) throw new Error('Failed to fetch notes');

        const notes = await response.json();
        return { notes };
    } catch (e) {
        throw error(500, 'Failed to load notes');
    }
};

/** @type {import('./$types').Actions} */
export const actions = {
    // Update note content
    update: async ({ request }) => {
        const data = await request.formData();

        const id = data.get('id');
        const content = data.get('content');
        const title = data.get('title');

        try {
            const response = await fetch(`${API_BASE_URL}/note/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, content })
            });

            if (!response.ok) throw new Error('Failed to update note');
            return { success: true };
        } catch (e) {
            return { success: false, error: e.message };
        }
    },

    delete: async ({ request }) => {
        const data = await request.formData();
        const id = data.get('id');

        try {
            const response = await fetch(`${API_BASE_URL}/note/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('Failed to delete note');
            return { success: true };
        } catch (e) {
            return { success: false, error: e.message };
        }
    },

    updateReminder: async ({ request }) => {
        const data = await request.formData();
        const noteId = data.get('noteId');
        const email = data.get('email');
        const reminderTime = data.get('reminderTime');
        const message = data.get('message');

        try {
            const response = await fetch(`${API_BASE_URL}/reminder/${noteId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email, 
                    message, 
                    reminder_time: reminderTime 
                })
            });

            if (!response.ok) throw new Error('Failed to update reminder.');
            return { success: true };
        } catch (e) {
            return { success: false, error: e.message };
        }
    },
}