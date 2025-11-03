(function () {
  const sidebar = document.getElementById('sidebar');
  const toggle = document.getElementById('menu-toggle');

  if (!sidebar || !toggle) return;

  toggle.addEventListener('click', function () {
    sidebar.classList.toggle('show');
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth >= 992) {
      sidebar.classList.remove('show');
    }
  });
})();
