 document.addEventListener("DOMContentLoaded", () => {
        const boxes = document.querySelectorAll(".box");
        const applyZoom = () => {
          boxes.forEach((box) => {
            // Check if the box is in the viewport
            if (box.getBoundingClientRect().top < window.innerHeight) {
              box.classList.add("zoom-in");
            }
          });
        };

        // Initial zoom effect
        applyZoom();

        // Add zoom-in effect on scroll
        window.addEventListener("scroll", applyZoom);
      });

      document.addEventListener("DOMContentLoaded", () => {
        const boxes = document.querySelectorAll(".boxex");

        const applyZoom = () => {
          boxes.forEach((box) => {
            const rect = box.getBoundingClientRect();
            // Check if the box is in the viewport
            if (rect.top < window.innerHeight && rect.bottom > 0) {
              box.classList.add("zoom-in");
            } else {
              box.classList.remove("zoom-in");
            }
          });
        };

        // Initial zoom effect
        applyZoom();

        // Add zoom-in effect on scroll
        window.addEventListener("scroll", applyZoom);
      });