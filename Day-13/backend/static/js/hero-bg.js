// hero-bg.js — ambient looping background animation for the hero section.
//
// There's no real background *video* file here (nothing to source it from),
// so instead this draws a lightweight, infinitely-looping canvas animation
// that behaves like one: it autoplays, loops, sits behind the hero content,
// and never needs controls. Visually it's small drifting "ticket" particles
// flowing left-to-right and occasionally linking up — a nod to what
// TicketSense actually does (tickets streaming in and getting routed),
// rendered in the site's own indigo / violet / teal palette.
(() => {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const ctx = canvas.getContext('2d');
  const COLORS = ['#7B5CFA', '#00C9A7', '#3AA0FF', '#4433B8'];

  let width = 0, height = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
  let particles = [];
  let raf = null;
  let running = true;

  function particleCount() {
    // Scale with area, capped for perf on big/ultrawide screens.
    return Math.min(70, Math.max(28, Math.round((width * height) / 26000)));
  }

  function makeParticle() {
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      vx: 0.15 + Math.random() * 0.35,
      vy: (Math.random() - 0.5) * 0.12,
      r: 1.2 + Math.random() * 1.8,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      pulse: Math.random() * Math.PI * 2,
    };
  }

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    width = Math.round(rect.width);
    height = Math.round(rect.height);
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const target = particleCount();
    if (particles.length < target) {
      while (particles.length < target) particles.push(makeParticle());
    } else {
      particles.length = target;
    }
  }

  function step() {
    ctx.clearRect(0, 0, width, height);

    // Update + draw links first (so dots sit on top)
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.pulse += 0.015;

      if (p.x > width + 20) {
        p.x = -20;
        p.y = Math.random() * height;
      }
      if (p.y < -20 || p.y > height + 20) {
        p.vy *= -1;
      }
    }

    const linkDist = 110;
    ctx.lineWidth = 1;
    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];
      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < linkDist) {
          const alpha = (1 - dist / linkDist) * 0.16;
          ctx.strokeStyle = `rgba(123, 92, 250, ${alpha})`;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      const glow = 0.55 + Math.sin(p.pulse) * 0.35;
      ctx.beginPath();
      ctx.fillStyle = p.color;
      ctx.globalAlpha = glow;
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    if (running) raf = requestAnimationFrame(step);
  }

  resize();
  raf = requestAnimationFrame(step);

  window.addEventListener('resize', () => {
    resize();
  });

  // Pause when the tab is hidden or the hero scrolls off-screen — keeps this
  // "video" from burning CPU/battery in the background, same as a real one would.
  document.addEventListener('visibilitychange', () => {
    running = !document.hidden;
    if (running && !raf) raf = requestAnimationFrame(step);
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        running = entry.isIntersecting && !document.hidden;
        if (running && !raf) raf = requestAnimationFrame(step);
      });
    }, { threshold: 0 });
    observer.observe(canvas);
  }
})();
