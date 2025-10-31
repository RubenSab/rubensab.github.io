document.addEventListener('DOMContentLoaded', () => {
  const images = document.querySelectorAll('.gallery img');

  images.forEach(img => {
    const classify = () => {
      // Skip if already classified
      if (img.classList.contains('landscape') || img.classList.contains('portrait')) return;

      // Make sure natural sizes are known
      if (img.naturalWidth && img.naturalHeight) {
        if (img.naturalWidth > img.naturalHeight) {
          img.classList.add('landscape');
        } else {
          img.classList.add('portrait');
        }
      }
    };

    if (img.complete) {
      classify();
    } else {
      img.addEventListener('load', classify);
    }
  });
});

