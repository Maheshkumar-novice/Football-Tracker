/**
 * Football Matches Tracker - Frontend JavaScript
 */

// 1. Initialize Tabs (Global function for onclick)
window.openTab = function (tabId) {
    // Hide all tab content
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    // Deactivate all tab buttons
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

    // Show selected tab content
    const content = document.getElementById(tabId);
    if (content) content.classList.add('active');

    // Activate clicked button
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        if (btn.getAttribute('onclick').includes(`'${tabId}'`)) {
            btn.classList.add('active');
        }
    });
};

document.addEventListener('DOMContentLoaded', () => {

    // 2. Initialize List.js for each competition
    const competitions = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL'];
    competitions.forEach(code => {
        const containerId = `standings-${code}`;
        if (document.getElementById(containerId)) {
            new List(containerId, {
                valueNames: ['rank', 'team', 'played', 'won', 'draw', 'lost', 'gf', 'ga', 'gd', 'points']
            });
        }
    });

    // 3. Render AI Summary Markdown
    const summaryTextEl = document.querySelector('.summary-text');
    if (summaryTextEl) {
        // Get raw markdown content
        const rawMarkdown = summaryTextEl.textContent.trim();
        // Parse and render HTML
        if (rawMarkdown) {
            summaryTextEl.innerHTML = marked.parse(rawMarkdown);
        }
    }
});
