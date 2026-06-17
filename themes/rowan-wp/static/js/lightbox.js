// Lightbox for image galleries
(function() {
  'use strict';

  var overlay = null;
  var closeBtn = null;

  function initLightbox() {
    // Create overlay element
    overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.style.display = 'none';
    overlay.addEventListener('click', closeLightbox);
    document.body.appendChild(overlay);

    closeBtn = document.createElement('div');
    closeBtn.className = 'lightbox-close';
    closeBtn.textContent = 'X';
    closeBtn.style.display = 'none';
    closeBtn.addEventListener('click', closeLightbox);
    document.body.appendChild(closeBtn);

    // Close on escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeLightbox();
    });

    // Bind all lightbox links
    bindLinks();
  }

  function bindLinks() {
    var links = document.querySelectorAll('a.lightbox, a.lightbox-gallery');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function(e) {
        e.preventDefault();
        openLightbox(this.getAttribute('href'));
      });
    }
  }

  function openLightbox(src) {
    var img = document.createElement('img');
    img.src = src;
    img.alt = '';
    overlay.innerHTML = '';
    overlay.appendChild(img);
    overlay.style.display = 'flex';
    closeBtn.style.display = 'block';
  }

  function closeLightbox() {
    overlay.style.display = 'none';
    closeBtn.style.display = 'none';
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLightbox);
  } else {
    initLightbox();
  }
})();
