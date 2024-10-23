import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export const load = async ({ fetch }) => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/notes');
        if (!response.ok) throw new Error('Failed to fetch notes');

        const notes = await response.json();
        return { notes };
    } catch (e) {
        throw error(500, 'Failed to load notes');
    }
};