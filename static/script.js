/**
 * Auto-refresh functionality for Football Matches Tracker
 * Reloads the page every 30 minutes to fetch updated match data
 */

// Auto-refresh interval: 30 minutes in milliseconds
const REFRESH_INTERVAL = 30 * 60 * 1000; // 30 minutes

// Schedule page reload
setTimeout(() => {
    console.log('Auto-refreshing page to fetch latest match data...');
    window.location.reload();
}, REFRESH_INTERVAL);

// Log the auto-refresh setup for debugging
console.log(`Auto-refresh scheduled for ${REFRESH_INTERVAL / 1000 / 60} minutes from now`);

// Add keyboard support for match rows
document.addEventListener('DOMContentLoaded', () => {
    const matchRows = document.querySelectorAll('.match-row');

    matchRows.forEach(row => {
        row.addEventListener('keypress', (event) => {
            // Trigger click on Enter or Space
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                row.click();
            }
        });
    });
});
