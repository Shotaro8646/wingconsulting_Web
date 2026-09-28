(() => {
  const dialog = document.querySelector('#diagram-dialog');
  if (!dialog || !dialog.showModal) return;
  const picture = dialog.querySelector('img');
  const title = dialog.querySelector('h2');
  document.querySelectorAll('[data-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      picture.src = button.dataset.zoom;
      picture.alt = button.dataset.title;
      title.textContent = button.dataset.title;
      dialog.showModal();
      const scroll = dialog.querySelector('.diagram-scroll');
      scroll.scrollTop = 0;
      scroll.scrollLeft = 0;
    });
  });
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
})();