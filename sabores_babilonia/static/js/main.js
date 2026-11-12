(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EMOJIS = ['🍃', '🌸', '🌼', '✨', '🍂'];

  document.querySelectorAll('.btn').forEach(btn => {
    // 1) Onda al hacer clic
    btn.addEventListener('click', e => {
      const r = btn.getBoundingClientRect();
      const size = Math.max(r.width, r.height);
      const el = document.createElement('span');
      el.className = 'ripple';
      el.style.width = el.style.height = size + 'px';
      el.style.left = e.clientX - r.left - size / 2 + 'px';
      el.style.top = e.clientY - r.top - size / 2 + 'px';
      btn.appendChild(el);
      el.addEventListener('animationend', () => el.remove());

      // 2) Lluvia de pétalos y hojas
      if (reduce) return;
      for (let i = 0; i < 8; i++) {
        const p = document.createElement('span');
        p.className = 'petal';
        p.textContent = EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
        p.style.left = e.clientX + 'px';
        p.style.top = e.clientY + 'px';
        p.style.setProperty('--dx', (Math.random() * 160 - 80) + 'px');
        p.style.setProperty('--dy', (Math.random() * -120 - 20) + 'px');
        p.style.setProperty('--rot', (Math.random() * 360) + 'deg');
        document.body.appendChild(p);
        p.addEventListener('animationend', () => p.remove());
      }
    });

    // 3) Efecto magnético: el botón sigue suavemente al cursor
    if (reduce) return;
    btn.addEventListener('mousemove', e => {
      const r = btn.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width / 2) * 0.15;
      const y = (e.clientY - r.top - r.height / 2) * 0.25;
      btn.style.transform = `translate(${x}px, ${y - 3}px) scale(1.04)`;
    });
    btn.addEventListener('mouseleave', () => (btn.style.transform = ''));
  });
})();
