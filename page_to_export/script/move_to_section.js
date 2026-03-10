function scrollToSection(targetId) {
    const target = document.getElementById(targetId);
    if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}