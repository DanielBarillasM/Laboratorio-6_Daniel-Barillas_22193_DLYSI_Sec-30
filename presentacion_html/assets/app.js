(() => {
  "use strict";

  const slides = Array.from(document.querySelectorAll(".slide"));
  const body = document.body;
  const previousButton = document.querySelector("#previous-button");
  const nextButton = document.querySelector("#next-button");
  const currentLabel = document.querySelector("#current-slide");
  const totalLabel = document.querySelector("#total-slides");
  const railList = document.querySelector("#rail-list");
  const railProgress = document.querySelector("#rail-progress");
  const tocDialog = document.querySelector("#toc-dialog");
  const tocButton = document.querySelector("#toc-button");
  const tocClose = document.querySelector("#toc-close");
  const tocList = document.querySelector("#toc-list");
  const notesButton = document.querySelector("#notes-button");
  const fullscreenButton = document.querySelector("#fullscreen-button");

  let currentIndex = 0;
  let touchStartX = null;

  const pad = (number) => String(number).padStart(2, "0");

  function indexFromHash() {
    const match = window.location.hash.match(/^#slide-(\d{2})$/);
    if (!match) return 0;
    return Math.min(Math.max(Number(match[1]) - 1, 0), slides.length - 1);
  }

  function buildNavigation() {
    totalLabel.textContent = pad(slides.length);
    slides.forEach((slide, index) => {
      const title = slide.dataset.title || `Diapositiva ${index + 1}`;
      const railItem = document.createElement("li");
      const railButton = document.createElement("button");
      railButton.type = "button";
      railButton.setAttribute("aria-label", `${pad(index + 1)}. ${title}`);
      railButton.title = title;
      railButton.addEventListener("click", () => showSlide(index));
      railItem.append(railButton);
      railList.append(railItem);

      const tocItem = document.createElement("li");
      const tocLink = document.createElement("a");
      tocLink.href = `#slide-${pad(index + 1)}`;
      tocLink.innerHTML = `<span class="toc-number">${pad(index + 1)}</span><span class="toc-name">${title}</span>`;
      tocLink.addEventListener("click", () => {
        tocDialog.close();
        showSlide(index);
      });
      tocItem.append(tocLink);
      tocList.append(tocItem);
    });
  }

  function showSlide(index, options = {}) {
    const { updateHash = true, focus = false } = options;
    currentIndex = Math.min(Math.max(index, 0), slides.length - 1);
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === currentIndex;
      slide.classList.toggle("is-active", active);
      slide.classList.remove("is-entering");
      slide.setAttribute("aria-hidden", String(!active));
      if (active) requestAnimationFrame(() => slide.classList.add("is-entering"));
    });

    railList.querySelectorAll("button").forEach((button, buttonIndex) => {
      if (buttonIndex === currentIndex) button.setAttribute("aria-current", "step");
      else button.removeAttribute("aria-current");
      button.classList.toggle("is-visited", buttonIndex < currentIndex);
    });
    tocList.querySelectorAll("a").forEach((link, linkIndex) => {
      if (linkIndex === currentIndex) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });

    currentLabel.textContent = pad(currentIndex + 1);
    previousButton.disabled = currentIndex === 0;
    nextButton.disabled = currentIndex === slides.length - 1;
    railProgress.style.height = `${slides.length === 1 ? 100 : currentIndex / (slides.length - 1) * 100}%`;
    if (updateHash) history.replaceState(null, "", `#slide-${pad(currentIndex + 1)}`);
    document.title = `${pad(currentIndex + 1)} · ${slides[currentIndex].dataset.title} · Calculadora Neuronal`;

    if (focus) {
      const heading = slides[currentIndex].querySelector("h1, h2");
      if (heading) {
        heading.tabIndex = -1;
        heading.focus({ preventScroll: true });
      }
    }
  }

  const changeSlide = (delta) => showSlide(currentIndex + delta, { focus: true });

  function toggleNotes() {
    const visible = body.classList.toggle("show-notes");
    notesButton.setAttribute("aria-pressed", String(visible));
  }

  async function toggleFullscreen() {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen?.();
    else await document.exitFullscreen?.();
  }

  function updateFullscreenLabel() {
    const active = Boolean(document.fullscreenElement);
    fullscreenButton.setAttribute("aria-label", active ? "Salir de pantalla completa" : "Activar pantalla completa");
    fullscreenButton.title = active ? "Salir de pantalla completa (F)" : "Pantalla completa (F)";
  }

  function openToc() {
    if (!tocDialog.open) tocDialog.showModal();
  }

  previousButton.addEventListener("click", () => changeSlide(-1));
  nextButton.addEventListener("click", () => changeSlide(1));
  notesButton.addEventListener("click", toggleNotes);
  fullscreenButton.addEventListener("click", toggleFullscreen);
  tocButton.addEventListener("click", openToc);
  tocClose.addEventListener("click", () => tocDialog.close());
  document.addEventListener("fullscreenchange", updateFullscreenLabel);
  tocDialog.addEventListener("click", (event) => { if (event.target === tocDialog) tocDialog.close(); });
  window.addEventListener("hashchange", () => showSlide(indexFromHash(), { updateHash: false }));

  document.addEventListener("keydown", (event) => {
    if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;
    if (["ArrowRight", "PageDown"].includes(event.key) || (event.key === " " && !event.shiftKey)) {
      event.preventDefault(); changeSlide(1);
    } else if (["ArrowLeft", "PageUp"].includes(event.key) || (event.key === " " && event.shiftKey)) {
      event.preventDefault(); changeSlide(-1);
    } else if (event.key === "Home") {
      event.preventDefault(); showSlide(0, { focus: true });
    } else if (event.key === "End") {
      event.preventDefault(); showSlide(slides.length - 1, { focus: true });
    } else if (event.key.toLowerCase() === "f") {
      event.preventDefault(); toggleFullscreen();
    } else if (event.key.toLowerCase() === "g") {
      event.preventDefault(); toggleNotes();
    } else if (event.key.toLowerCase() === "o") {
      event.preventDefault(); openToc();
    }
  });

  document.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0]?.clientX ?? null;
  }, { passive: true });
  document.addEventListener("touchend", (event) => {
    if (touchStartX === null) return;
    const touchEndX = event.changedTouches[0]?.clientX ?? touchStartX;
    const distance = touchEndX - touchStartX;
    if (Math.abs(distance) > 60) changeSlide(distance < 0 ? 1 : -1);
    touchStartX = null;
  }, { passive: true });

  buildNavigation();
  body.classList.add("deck-ready");
  showSlide(indexFromHash(), { updateHash: !window.location.hash });
})();
