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