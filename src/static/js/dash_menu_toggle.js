document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById('menu-btn');
  const asideMenu = document.getElementById('aside-menu');
  const overlay = document.getElementById('overlay');

  if (menuBtn && asideMenu && overlay) {
    menuBtn.onclick = () => {
      asideMenu.classList.toggle('-translate-x-full');
      overlay.classList.toggle('hidden');
    }

    overlay.onclick = () => {
      asideMenu.classList.add('-translate-x-full');
      overlay.classList.add('hidden');
    }
  }
});