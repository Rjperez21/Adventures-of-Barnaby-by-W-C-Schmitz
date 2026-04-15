// Scrollytelling reveal — each .scene fades in when well into the viewport.
// Uses IntersectionObserver; no dependencies.

(function () {
  const scenes = document.querySelectorAll('.scene');
  if (!scenes.length) return;

  // Respect reduced motion — just mark everything in-view immediately.
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) {
    scenes.forEach(s => s.classList.add('in-view'));
    return;
  }

  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      // Trigger once we're ~30% into the section so the reveal feels "earned"
      if (entry.isIntersecting && entry.intersectionRatio >= 0.28) {
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    }
  }, {
    threshold: [0, 0.15, 0.28, 0.5, 0.75, 1],
    // Slight negative bottom margin delays activation until scrolled further in
    rootMargin: '0px 0px -12% 0px'
  });

  scenes.forEach(s => io.observe(s));
})();
