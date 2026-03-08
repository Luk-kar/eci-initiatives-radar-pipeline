async function loadPartial(url, targetId) {
    const res = await fetch(url);
    const html = await res.text();
    const target = document.getElementById(targetId);
    target.innerHTML = html;
    target.querySelectorAll("script").forEach(old => {
        const s = document.createElement("script");
        s.textContent = old.textContent;
        old.replaceWith(s);
    });
}

(async () => {
    await loadPartial("partials/header.html", "header-slot");
    await loadPartial("partials/deep_dive_footer.html", "footer-slot");
    await loadPartial("partials/kpi_row.html", "kpi-slot");
    await loadPartial("partials/chart_top_10_signatures.html", "chart1-slot");
    await loadPartial("partials/chart_outcomes.html", "chart-initiatives-status-slot");
    await loadPartial("partials/chart_signatures_cohorts.html", "chart-signatures-count-slot");
    await loadPartial("partials/list_currently_open.html", "currently-open");
})();