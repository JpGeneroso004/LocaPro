// Art.Tendas — JS utilitário

// Auto-dismiss messages after 5s
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      alert.style.transition = '0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });
});

// ── Data BR (DD/MM/AAAA) — avanço automático entre campos ──
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.data-br-wrapper').forEach(wrapper => {
    const dia = wrapper.querySelector('.data-dia');
    const mes = wrapper.querySelector('.data-mes');
    const ano = wrapper.querySelector('.data-ano');
    if (!dia || !mes || !ano) return;

    const apenasNumeros = (e) => {
      e.target.value = e.target.value.replace(/[^0-9]/g, '');
    };

    dia.addEventListener('input', (e) => {
      apenasNumeros(e);
      if (e.target.value.length >= 2) mes.focus();
    });

    mes.addEventListener('input', (e) => {
      apenasNumeros(e);
      if (e.target.value.length >= 2) ano.focus();
    });

    ano.addEventListener('input', (e) => {
      apenasNumeros(e);
      if (e.target.value.length >= 4) ano.blur();
    });

    // Backspace no campo vazio volta para o anterior
    mes.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && e.target.value === '') dia.focus();
    });
    ano.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && e.target.value === '') mes.focus();
    });
  });
});
