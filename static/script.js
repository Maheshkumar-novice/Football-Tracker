/**
 * Football Matches Tracker - Frontend JavaScript
 * Handles auto-refresh and AI summary generation
 */

// Auto-refresh interval: 30 minutes in milliseconds
const REFRESH_INTERVAL = 30 * 60 * 1000; // 30 minutes

// Track summary generation state
let summaryGenerated = false;
let summaryGeneratedAt = null;

/**
 * Check if summary is currently visible
 */
function isSummaryVisible() {
    const summaryBlock = document.getElementById('summary-block');
    return summaryBlock && summaryBlock.style.display !== 'none';
}

/**
 * Show the reload banner
 */
function showReloadBanner() {
    const banner = document.getElementById('reload-banner');
    if (banner) {
        banner.style.display = 'block';
        console.log('Reload banner displayed');
    }
}

/**
 * Calculate relative time string
 */
function getRelativeTime(isoTimestamp) {
    const now = new Date();
    const then = new Date(isoTimestamp);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins === 1) return '1 minute ago';
    if (diffMins < 60) return `${diffMins} minutes ago`;

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours === 1) return '1 hour ago';
    return `${diffHours} hours ago`;
}

/**
 * Generate AI summary
 */
async function generateSummary() {
    console.log('Generate Summary button clicked');

    const button = document.getElementById('generate-summary-btn');
    const loading = document.getElementById('summary-loading');
    const errorDiv = document.getElementById('summary-error');
    const summaryBlock = document.getElementById('summary-block');

    // Change button state
    button.textContent = 'Generating…';
    button.disabled = true;

    // Show loading, hide others
    loading.style.display = 'block';
    errorDiv.style.display = 'none';
    summaryBlock.style.display = 'none';

    try {
        // Make POST request
        const response = await fetch('/generate-summary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        // Hide loading
        loading.style.display = 'none';

        if (data.success) {
            // Display summary
            const summaryText = document.getElementById('summary-text');
            const summaryTimestamp = document.getElementById('summary-timestamp');

            summaryText.textContent = data.summary;
            summaryTimestamp.textContent = `Summary generated ${getRelativeTime(data.generated_at)}`;

            summaryBlock.style.display = 'block';

            // Update button state
            button.textContent = 'Summary available after next update';
            summaryGenerated = true;
            summaryGeneratedAt = data.generated_at;

            // Store in sessionStorage
            sessionStorage.setItem('summaryGenerated', 'true');

            console.log('Summary generated and displayed successfully');
        } else {
            // Show error
            errorDiv.textContent = data.error || 'Failed to generate summary. Please try again.';
            errorDiv.style.display = 'block';

            // Re-enable button
            button.textContent = 'Generate Summary';
            button.disabled = false;

            console.error('Summary generation failed:', data.error);
        }
    } catch (error) {
        // Handle fetch error
        loading.style.display = 'none';
        errorDiv.textContent = 'Unable to connect. Please try again.';
        errorDiv.style.display = 'block';

        // Re-enable button
        button.textContent = 'Generate Summary';
        button.disabled = false;

        console.error('Error generating summary:', error);
    }
}

// Auto-refresh logic with summary override
setTimeout(() => {
    if (isSummaryVisible()) {
        // Show reload banner instead of auto-reloading
        console.log('Summary visible - showing reload banner instead of auto-refresh');
        showReloadBanner();
    } else {
        // Normal auto-refresh
        console.log('Auto-refreshing page to fetch latest match data...');
        window.location.reload();
    }
}, REFRESH_INTERVAL);

// Log the auto-refresh setup for debugging
console.log(`Auto-refresh scheduled for ${REFRESH_INTERVAL / 1000 / 60} minutes from now`);

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add keyboard support for match rows
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

    // Add event listener for Generate Summary button
    const summaryButton = document.getElementById('generate-summary-btn');
    if (summaryButton) {
        summaryButton.addEventListener('click', generateSummary);
        console.log('Summary button event listener attached');
    }

    // Check sessionStorage for previous summary state
    if (sessionStorage.getItem('summaryGenerated') === 'true') {
        summaryButton.disabled = true;
        summaryButton.textContent = 'Summary available after next update';
        console.log('Previous summary state restored from sessionStorage');
    }

    // Clear sessionStorage on manual reload (indicates new data)
    window.addEventListener('beforeunload', () => {
        sessionStorage.removeItem('summaryGenerated');
    });
});
