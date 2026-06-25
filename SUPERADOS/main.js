// Marie Kids Catalog - main.js

document.addEventListener('DOMContentLoaded', function () {

  // ── Botón exportar PDF ──────────────────────────────────────────
  const btnPdf = document.querySelector('.btn-pdf');
  if (btnPdf) {
    btnPdf.addEventListener('click', function () {
      window.print();
    });
  }

  // ── Contar páginas y mostrar en toolbar ────────────────────────
  const pages = document.querySelectorAll('.page');
  const hint  = document.querySelector('.toolbar-hint');
  if (hint && pages.length) {
    hint.textContent = 'Vista libro A4 · ' + pages.length + ' páginas';
  }

});
