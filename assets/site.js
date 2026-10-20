// Shared by every page: links open in a new tab, book links jump to the right PDF page,
// and long pages get a table of contents.
(function () {
  const BOOK = "https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf";
  const BOOK_API = "https://api.github.com/repos/AjaySingh10/interview-prep-books/contents/system-design-interview-vol1.pdf";
  const token = () => { try { return localStorage.getItem("iprep.token") || ""; } catch { return ""; } };

  // The book is in a private repo. With the tracker's GitHub token we download it once
  // (cached in the browser) and open it at the exact page; without one, GitHub's viewer opens.
  let bookUrl = null;
  async function loadBook() {
    if (bookUrl) return bookUrl;
    const cache = "caches" in window ? await caches.open("iprep-books").catch(() => null) : null;
    let res = cache && await cache.match(BOOK_API);
    if (!res) {
      res = await fetch(BOOK_API, { headers: { Authorization: `Bearer ${token()}`, Accept: "application/vnd.github.raw" } });
      if (!res.ok) throw new Error(`GitHub returned ${res.status}`);
      if (cache) await cache.put(BOOK_API, res.clone()).catch(() => {});
    }
    bookUrl = URL.createObjectURL(new Blob([await res.arrayBuffer()], { type: "application/pdf" }));
    return bookUrl;
  }
  function openBook(page) {
    const win = window.open("", "_blank");
    if (!win) return false;
    win.document.title = "Opening book…";
    win.document.body.innerHTML = `<p style="font:16px system-ui,sans-serif;padding:24px">Opening the book${page ? ` at page ${page}` : ""}…</p>`;
    loadBook()
      .then(url => { win.location.href = url + (page ? `#page=${page}` : ""); })
      .catch(() => { win.location.href = BOOK; });
    return true;
  }

  document.addEventListener("click", e => {
    const a = e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.getAttribute("href").startsWith("#")) return;
    if (a.href.startsWith(BOOK) && token()) {
      const page = (a.hash.match(/page=(\d+)/) || [])[1];
      if (openBook(page)) { e.preventDefault(); return; }
    }
    a.target = "_blank";
    a.rel = "noopener";
  });

  function decorate(root) {
    for (const a of root.querySelectorAll(`a[href^="${BOOK}"]:not(.card)`)) {
      const page = (a.hash.match(/page=(\d+)/) || [])[1];
      a.classList.add("book-link");
      a.title = `Alex Xu Vol 1${page ? `, page ${page}` : ""} (private — opens for you only)`;
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
