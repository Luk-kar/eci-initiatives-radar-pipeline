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
    for (const [url, id] of [...STATIC_PARTIALS, ...GENERATED_PARTIALS]) {
        await loadPartial(url, id);
    }
})();