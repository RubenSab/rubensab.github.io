document.addEventListener('DOMContentLoaded', () => {
  const images = document.querySelectorAll('.gallery img');
  images.forEach(img => {
    const classify = () => {
      // Skip if has 'full' attribute
      if (img.hasAttribute('full')) {
        img.classList.add('landscape');
        return;
      }
      if (img.hasAttribute('vertical')) {
        img.classList.add('portrait');
        return;
      }
      
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
    
    // Add click event to toggle between landscape and portrait
    img.addEventListener('click', () => {
      if (img.classList.contains('landscape')) {
        img.classList.remove('landscape');
        img.classList.add('portrait');
      } else if (img.classList.contains('portrait')) {
        img.classList.remove('portrait');
        img.classList.add('landscape');
      }
    });
  });
});
