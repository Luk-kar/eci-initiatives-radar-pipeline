const MS_PER_SECOND = 1000;
const MS_PER_MINUTE = 1000 * 60;
const MS_PER_HOUR = 1000 * 60 * 60;
const MS_PER_DAY = 1000 * 60 * 60 * 24;


function parseDate(str) {
    const [day, month, year] = str.split("/").map(Number);
    return new Date(year, month - 1, day);
}


/**
 * Returns the next Sunday midnight at or after the given date.
 * Used to detect the weekly Sunday night data refresh window.
 */
function getNextSundayAfter(date) {
    const result = new Date(date);
    const dayOfWeek = result.getDay(); // 0 = Sunday
    const daysUntilSunday = dayOfWeek === 0 ? 0 : 7 - dayOfWeek;
    result.setDate(result.getDate() + daysUntilSunday);
    result.setHours(0, 0, 0, 0);
    return result;
}


/**
 * Returns a human-readable time label given a millisecond difference.
 * Used for both "X left" and "starts in X" countdowns.
 * @param {number} diffMs - positive number of milliseconds
 */
function formatTimeDiff(diffMs) {
    const diffSecs = Math.floor(diffMs / MS_PER_SECOND);
    const diffMins = Math.floor(diffMs / MS_PER_MINUTE);
    const diffHours = Math.floor(diffMs / MS_PER_HOUR);
    const diffDays = Math.round(diffMs / MS_PER_DAY);

    if (diffMs < MS_PER_MINUTE) return `${diffSecs} second${diffSecs !== 1 ? "s" : ""}`;
    if (diffMins === 1) return "1 min";
    if (diffHours < 1) return `${diffMins} mins`;
    if (diffHours === 1) return "1 hour";
    if (diffDays === 0) return `${diffHours} hours`;
    return `${diffDays} day${diffDays !== 1 ? "s" : ""}`;
}


/**
 * Returns a human-readable label for time left until start + 12 months.
 * @param {string} startStr   - e.g. "04/02/2026" (DD/MM/YYYY)
 * @param {string} closedStr  - e.g. "14/09/2026" or "" if not yet known
 * @param {Date}   now        - defaults to current time (injectable for testing)
 */
function getDaysLeftLabel(startStr, closedStr = "", now = new Date()) {

    if (!startStr) return "";

    const [day, month, year] = startStr.split("/").map(Number);
    const startDate = new Date(year, month - 1, day);
    const deadlineDate = new Date(year, month - 1 + 12, day);

    // Case 0: collection hasn't started yet → "starts in X"
    //
    // Ideally rows with a future start date should never reach this function
    // with a status of "Collection Ongoing" — the data pipeline should reflect
    // the correct status. However, this guard acts as a defensive fallback:
    // if the status label is stale or incorrectly set upstream, we still
    // render a meaningful "starts in X" label rather than a misleading countdown
    // to the 12-month deadline.
    if (now < startDate) {
        const diffMs = startDate - now;
        return `starts in ${formatTimeDiff(diffMs)}`;
    }

    // Case 1: closed date is known and has passed → always closed
    if (closedStr) {
        const closedDate = parseDate(closedStr);
        if (now >= closedDate) return "closed";
    }

    // Case 2: no closed date set, but past next Sunday after deadline
    // → data refresh happened and initiative was not closed → extended
    if (!closedStr) {
        const nextSunday = getNextSundayAfter(deadlineDate);
        if (now > nextSunday) return "extended";
    }

    // Case 3: normal countdown to deadline
    const diffMs = deadlineDate - now;
    const diffDays = Math.round(diffMs / MS_PER_DAY);

    if (diffMs < 0) return diffDays !== 0
        ? `closed ${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? "s" : ""} ago`
        : "closed";

    return formatTimeDiff(diffMs);
}


document.addEventListener("DOMContentLoaded", () => {
    function update() {
        document.querySelectorAll(".days-left-cell").forEach(cell => {
            const label = cell.querySelector(".days-left-cell__label");
            if (!label || !cell.dataset.start) return;
            label.textContent = getDaysLeftLabel(cell.dataset.start, cell.dataset.closed);
        });
    }

    update();
    setInterval(update, 1000);
});


// start "04/02/2026" → deadline 2027-02-04 (Thu) → next Sunday 2027-02-07


function runDaysLeftLabelTests() {
    const failures = [];

    // --- future start date ---
    test(failures, "starts in 30 days", "04/04/2026", "", new Date("2026-03-05"), "starts in 30 days");
    test(failures, "starts in 1 day", "04/04/2026", "", new Date("2026-04-03"), "starts in 1 day");
    test(failures, "starts in 1 hour", "04/04/2026", "", new Date("2026-04-03T23:00:00"), "starts in 1 hour");
    test(failures, "starts in 45 mins", "04/04/2026", "", new Date("2026-04-03T23:15:00"), "starts in 45 mins");
    test(failures, "starts in 1 second", "04/04/2026", "", new Date("2026-04-03T23:59:59"), "starts in 1 second");

    // --- existing cases (no closed date) ---
    test(failures, "1 day left", "04/02/2026", "", new Date("2027-02-03"), "1 day");
    test(failures, "365 days left", "04/02/2026", "", new Date("2026-02-04"), "365 days");
    test(failures, "29 seconds", "04/02/2026", "", new Date("2027-02-03T23:59:31"), "29 seconds");
    test(failures, "1 hour", "04/02/2026", "", new Date("2027-02-03T23:00:00"), "1 hour");

    // --- data-closed empty, deadline passed, before Sunday refresh ---
    test(failures, "deadline passed, awaiting refresh", "04/02/2026", "", new Date("2027-02-04T06:00:00"), "closed");

    // --- data-closed empty, past next Sunday → extended ---
    test(failures, "extended", "04/02/2026", "", new Date("2027-02-08"), "extended");

    // --- data-closed set, not yet reached → normal countdown ---
    test(failures, "closed date set, not yet", "04/02/2026", "04/02/2027", new Date("2027-02-03"), "1 day");

    // --- data-closed set and passed → closed ---
    test(failures, "closed by date", "04/02/2026", "01/06/2026", new Date("2026-07-01"), "closed");

    // --- diffMs < 0 branch: closed N days ago ---
    test(failures, "closed 1 day ago", "04/02/2026", "", new Date("2027-02-05T12:00:00"), "closed 1 day ago");
    test(failures, "closed 3 days ago", "04/02/2026", "", new Date("2027-02-07T00:00:00"), "closed 3 days ago");
    test(failures, "closed 0 days ago", "04/02/2026", "", new Date("2027-02-04T00:30:00"), "closed");

    // --- boundary: exactly 1 minute left ---
    test(failures, "exactly 1 min", "04/02/2026", "", new Date("2027-02-03T23:59:00"), "1 min");

    // --- boundary: a few minutes left ---
    test(failures, "45 mins left", "04/02/2026", "", new Date("2027-02-03T23:15:00"), "45 mins");

    // --- boundary: exactly 1 hour left ---
    test(failures, "exactly 1 hour", "04/02/2026", "", new Date("2027-02-03T23:00:00"), "1 hour");

    // --- boundary: several hours left ---
    test(failures, "3 hours left", "04/02/2026", "", new Date("2027-02-03T21:00:00"), "3 hours");

    // --- boundary: exactly 1 second left ---
    test(failures, "1 second left", "04/02/2026", "", new Date("2027-02-03T23:59:59"), "1 second");

    if (failures.length > 0) {
        throw new Error(`❌ ${failures.length} test(s) failed:\n${failures.join("\n")}`);
    }
    console.log("✅ All tests passed");
}


function test(failures, label, startStr, closedStr, now, expected) {
    const [day, month, year] = startStr.split("/").map(Number);
    const deadline = new Date(year, month - 1 + 12, day);

    const result = getDaysLeftLabel(startStr, closedStr, now);

    const is_passed = result === expected;
    const label_acceptance = is_passed ? "✅" : "❌";

    console.group(`${label_acceptance} 🧪 [${label}]`);
    console.log(`  start:    ${startStr}`);
    console.log(`  closed:   ${closedStr || "(empty)"}`);
    console.log(`  deadline: ${formatDate(deadline)} (start + 12 months)`);
    console.log(`  now:      ${formatDate(now)}`);
    console.log(`  expected: "${expected}"`);

    if (!is_passed) {
        console.error(`  ❌ got: "${result}"`);
        console.groupEnd();
        failures.push(`[${label}] expected "${expected}", got "${result}"`);
        return;
    }

    console.log(`  ✅ got: "${result}"`);
    console.groupEnd();
}

function formatDate(date) {
    return date.toISOString().replace("T", " ").slice(0, 19);
}
