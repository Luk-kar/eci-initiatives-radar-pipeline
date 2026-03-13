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
 * Returns a human-readable label for time left until start + 12 months.
 * @param {string} startStr   - e.g. "04/02/2026" (DD/MM/YYYY)
 * @param {string} closedStr  - e.g. "14/09/2026" or "" if not yet known
 * @param {Date}   now        - defaults to current time (injectable for testing)
 */
function getDaysLeftLabel(startStr, closedStr = "", now = new Date()) {
    const [day, month, year] = startStr.split("/").map(Number);
    const deadlineDate = new Date(year, month - 1 + 12, day);

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
    const diffSecs = Math.floor(diffMs / MS_PER_SECOND);
    const diffMins = Math.floor(diffMs / MS_PER_MINUTE);
    const diffHours = Math.floor(diffMs / MS_PER_HOUR);
    const diffDays = Math.round(diffMs / MS_PER_DAY);

    if (diffMs < 0) return "closed";
    if (diffMs < MS_PER_MINUTE) return `${diffSecs} second${diffSecs !== 1 ? "s" : ""}`;
    if (diffMins === 1) return "1 min";
    if (diffHours < 1) return `${diffMins} mins`;
    if (diffHours === 1) return "1 hour";
    if (diffDays === 0) return `${diffHours} hours`;
    return `${diffDays} day${diffDays !== 1 ? "s" : ""}`;
}

document.addEventListener("DOMContentLoaded", () => {
    function update() {
        document.querySelectorAll(".days-left-cell").forEach(cell => {
            cell.textContent = getDaysLeftLabel(cell.dataset.start, cell.dataset.closed);
        });
    }
    update();
    setInterval(update, 1000);
});

// start "04/02/2026" → deadline 2027-02-04 (Thu) → next Sunday 2027-02-07

function runTests() {
    const failures = [];

    // --- existing cases (no closed date) ---
    test(failures, "1 day left", "04/02/2026", "", new Date("2027-02-03"), "1 day");
    test(failures, "365 days left", "04/02/2026", "", new Date("2026-02-04"), "365 days");
    test(failures, "29 seconds", "04/02/2026", "", new Date("2027-02-03T23:59:31"), "29 seconds");
    test(failures, "1 hour", "04/02/2026", "", new Date("2027-02-03T23:00:00"), "1 hour");

    // --- data-closed empty, deadline passed, before Sunday refresh ---
    test(failures, "deadline passed, awaiting refresh to next sunday", "04/02/2026", "", new Date("2027-02-05"), "closed");

    // --- data-closed empty, past next Sunday → extended ---
    test(failures, "extended, no closed collecting after deadline and refresh", "04/02/2026", "", new Date("2027-02-08"), "extended");

    // --- data-closed set, not yet reached → normal countdown ---
    test(failures, "closed date set, not yet, probably unlikely result", "04/02/2026", "04/02/2027", new Date("2027-02-03"), "1 day");

    // --- data-closed set and passed → closed ---
    test(failures, "closed by date", "04/02/2026", "01/06/2026", new Date("2026-07-01"), "closed");

    // ← NEW: throw once at the end summarising all failures, or confirm all passed
    if (failures.length > 0) {
        throw new Error(`❌ ${failures.length} test(s) failed:\n${failures.join("\n")}`);
    }
    console.log("✅ All tests passed"); // ← only reachable when failures is empty
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
