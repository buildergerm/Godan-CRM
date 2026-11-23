import * as publicEnv from '$app/env/public';
import { redirect, fail } from '@sveltejs/kit';
import axios from 'axios';
import { describeError } from '#lib/server/log-safe.js';
import type { Actions, PageServerLoad } from './$types';

type OnboardingAnswers = {
  role?: string;
  industry?: string;
  company_size?: string;
  goals?: string[];
  current_tool?: string;
  challenge?: string;
};

export const load: PageServerLoad = async ({ locals, cookies }) => {
  if (!locals.user) throw redirect(303, '/login');
  const token = cookies.get('jwt_access');
  if (!token) throw redirect(303, '/login');
  try {
    const response = await axios.get<{ answers: OnboardingAnswers; completed: boolean }>(publicEnv.PUBLIC_DJANGO_API_URL + '/api/auth/onboarding/', {
      headers: { Authorization: 'Bearer ' + token }
    });
    if (response.data.completed) throw redirect(303, '/org/new');
    return { answers: response.data.answers ?? {}, completed: false, unavailable: false };
  } catch (error) {
    if ((error as { status?: number }).status === 303) throw error;
    console.error('Onboarding load failed:', describeError(error));
    return { answers: {}, completed: false, unavailable: true };
  }
};

export const actions: Actions = {
  save: async ({ request, cookies, locals }) => {
    if (!locals.user) throw redirect(303, '/login');
    const token = cookies.get('jwt_access');
    if (!token) throw redirect(303, '/login');
    const form = await request.formData();
    let answers: unknown;
    try { answers = JSON.parse(String(form.get('answers') ?? '{}')); }
    catch { return fail(400, { saved: false, error: 'Please review your answers and try again.' }); }
    const completed = form.get('completed') === 'true';
    try {
      const response = await axios.patch<{ saved: boolean }>(publicEnv.PUBLIC_DJANGO_API_URL + '/api/auth/onboarding/', { answers, completed }, {
        headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' }
      });
      if (completed) throw redirect(303, '/org/new');
      return { saved: Boolean(response.data.saved), error: null };
    } catch (error) {
      if ((error as { status?: number }).status === 303) throw error;
      console.error('Onboarding save failed:', describeError(error));
      return fail(503, { saved: false, error: 'We could not save your progress. Please retry.' });
    }
  }
};
