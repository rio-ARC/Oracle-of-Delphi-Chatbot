/**
 * Oracle of Delphi — API Integration
 */

const API_URL = 'http://localhost:8000/chat';

let sessionId = sessionStorage.getItem('oracle_session') || 'session-' + Date.now();
sessionStorage.setItem('oracle_session', sessionId);

const input = document.getElementById('input');
const submitBtn = document.getElementById('submitBtn');
const questionEl = document.getElementById('question');
const responseEl = document.getElementById('response');
const parchment = document.querySelector('.parchment');

async function consult() {
    const text = input.value.trim();
    if (!text) {
        input.focus();
        return;
    }

    const question = text.endsWith('?') ? text : text + '?';
    questionEl.textContent = question;

    input.disabled = true;
    submitBtn.disabled = true;
    responseEl.innerHTML = '<p>...</p>';
    responseEl.classList.remove('fade-in');
    parchment.classList.add('contemplating');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: question, session_id: sessionId })
        });

        if (!response.ok) throw new Error('Oracle unavailable');

        const data = await response.json();
        responseEl.innerHTML = `<p>${data.response}</p>`;
        responseEl.classList.add('fade-in');

    } catch (error) {
        responseEl.innerHTML = '<p>The mists obscure the Oracle\'s vision. Try again...</p>';
        responseEl.classList.add('fade-in');
    } finally {
        parchment.classList.remove('contemplating');
        input.value = '';
        input.disabled = false;
        submitBtn.disabled = false;
        input.focus();
    }
}

submitBtn.addEventListener('click', consult);
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') consult();
});

window.addEventListener('load', () => input.focus());
