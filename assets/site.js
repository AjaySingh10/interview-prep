// Shared by every page: links open in a new tab, book links get a 📖 and a tooltip,
// and long pages get a table of contents.
(function () {
  // Book chapters live in a private repo, so these links only open for the owner.
  const BOOKS = "https://github.com/AjaySingh10/interview-prep-books/blob/main/";

  document.addEventListener("click", e => {
    const a = e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.getAttribute("href").startsWith("#")) return;
    a.target = "_blank";
    a.rel = "noopener";
  });

  function decorate(root) {
    for (const a of root.querySelectorAll(`a[href^="${BOOKS}"]:not(.card):not(.book-link)`)) {
      const ch = (a.pathname.match(/\/ch(\d+)-/) || [])[1];
      a.classList.add("book-link");
      a.title = `Alex Xu Vol 1${ch ? `, chapter ${+ch}` : ""} (private — opens for you only)`;
    }
  }

  function buildToc() {
    const content = document.querySelector(".page-content");
    const toc = document.getElementById("toc");
    if (!content || !toc) return;
    for (const t of content.querySelectorAll("table")) {
      const wrap = document.createElement("div");
      wrap.className = "table-wrap";
      t.replaceWith(wrap); wrap.appendChild(t);
      const head = t.querySelector("thead");
      if (head && !head.textContent.trim()) head.remove();
    }
    const heads = [...content.querySelectorAll("h2[id], h3[id]")];
    if (heads.length < 4) return;
    toc.innerHTML = heads.map(h => `<a href="#${h.id}" class="${h.tagName.toLowerCase()}">${h.textContent}</a>`).join("");
    const aside = document.querySelector(".toc");
    aside.hidden = false;
    aside.querySelector(".toc-title").addEventListener("click", e => {
      e.currentTarget.setAttribute("aria-expanded", aside.classList.toggle("open"));
    });
    toc.addEventListener("click", e => { if (e.target.closest("a")) aside.classList.remove("open"); });
    document.body.classList.add("has-toc");
    const links = new Map([...toc.querySelectorAll("a")].map(a => [a.getAttribute("href").slice(1), a]));
    const seen = new IntersectionObserver(entries => {
      for (const en of entries) if (en.isIntersecting) {
        toc.querySelectorAll("a.on").forEach(a => a.classList.remove("on"));
        const a = links.get(en.target.id);
        if (a) { a.classList.add("on"); a.scrollIntoView({ block: "nearest" }); }
      }
    }, { rootMargin: "-70px 0px -70% 0px" });
    heads.forEach(h => seen.observe(h));
  }

  function init() {
    decorate(document);
    buildToc();
    new MutationObserver(() => decorate(document)).observe(document.body, { childList: true, subtree: true });
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();
