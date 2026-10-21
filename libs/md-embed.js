/**
 * md-embed.js — вгражда съдържанието на .md файл вътре в урок.
 * Собствен (не CDN-вендорван) helper — изисква marked.js да е зареден преди него.
 *
 * Mermaid диаграми (```mermaid code block) и LaTeX формули ($..$ / $$..$$) се
 * засичат автоматично в текста и mermaid.js/KaTeX се зареждат мързеливо от
 * libs/ само когато реално има такова съдържание - няма нужда от допълнителни
 * <script> тагове в урока за това.
 *
 * YAML frontmatter с `toc: true` добавя бутон-хамбургер, който показва/скрива
 * съдържание (TOC), генерирано автоматично от h2/h3 заглавията в текста.
 *
 * Употреба:
 *   <div id="md-embed"></div>
 *   <script src="../../../libs/marked.min.js" onerror="this.onerror=null;this.src='https://unpkg.com/marked@12.0.2/marked.min.js'"></script>
 *   <script src="../../../libs/md-embed.js"></script>
 *   <script>
 *       document.addEventListener('DOMContentLoaded', function () {
 *           renderMarkdownEmbed('md-embed', 'статия.md');
 *       });
 *   </script>
 */
(function () {
    // Директорията, от която е зареден самият md-embed.js (т.е. libs/) -
    // използва се за да намерим mermaid.min.js / katex/ независимо от
    // дълбочината на урока спрямо repo root-а.
    var LIBS_BASE = (document.currentScript && document.currentScript.src)
        ? document.currentScript.src.replace(/md-embed\.js(?:\?.*)?$/, '')
        : '';

    var FRONTMATTER_RE = /^---\s*\n([\s\S]*?)\n---\s*\n?/;
    var MERMAID_RE = /```mermaid[\s\S]*?```/;
    var MATH_RE = /\$\$[\s\S]+?\$\$|\$[^\n$]+\$/;

    var loadedScripts = {};

    function loadScriptOnce(src) {
        if (loadedScripts[src]) return loadedScripts[src];
        loadedScripts[src] = new Promise(function (resolve, reject) {
            var script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = function () { reject(new Error('Неуспешно зареждане на ' + src)); };
            document.head.appendChild(script);
        });
        return loadedScripts[src];
    }

    function loadStylesheetOnce(href) {
        if (document.querySelector('link[href="' + href + '"]')) return;
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }

    function stripQuotes(value) {
        if (value.length >= 2 && value[0] === value[value.length - 1] && (value[0] === '"' || value[0] === "'")) {
            return value.slice(1, -1);
        }
        return value;
    }

    // Лек, line-based YAML frontmatter парсер - огледало на parse_frontmatter()
    // в build_library_manifest.py (не пълен YAML, достатъчен за key: value).
    function parseFrontmatter(raw) {
        var match = raw.match(FRONTMATTER_RE);
        if (!match) return { fields: {}, body: raw };

        var fields = {};
        match[1].split('\n').forEach(function (line) {
            line = line.trim();
            var idx = line.indexOf(':');
            if (!line || idx === -1) return;
            var key = line.slice(0, idx).trim().toLowerCase();
            fields[key] = stripQuotes(line.slice(idx + 1).trim());
        });

        return { fields: fields, body: raw.slice(match[0].length) };
    }

    function isTruthy(value) {
        return /^(true|yes|1)$/i.test(value || '');
    }

    function slugify(text) {
        return text.trim().toLowerCase()
            .replace(/[^\p{L}\p{N}]+/gu, '-')
            .replace(/^-+|-+$/g, '');
    }

    function renderMermaid(container) {
        if (!window.mermaid) return;
        var blocks = container.querySelectorAll('code.language-mermaid');
        blocks.forEach(function (codeEl) {
            var div = document.createElement('div');
            div.className = 'mermaid';
            div.textContent = codeEl.textContent;
            codeEl.parentElement.replaceWith(div);
        });
        if (!blocks.length) return;
        mermaid.initialize({ startOnLoad: false });
        mermaid.run({ nodes: container.querySelectorAll('.mermaid') });
    }

    function renderMath(container) {
        if (!window.renderMathInElement) return;
        renderMathInElement(container, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
            ],
        });
    }

    function setupToc(container) {
        var headings = container.querySelectorAll('h2, h3');
        if (!headings.length) return;

        var usedIds = {};
        var list = document.createElement('ul');

        headings.forEach(function (h) {
            if (!h.id) {
                var base = slugify(h.textContent) || 'section';
                var id = base;
                var n = 2;
                while (usedIds[id]) { id = base + '-' + (n++); }
                usedIds[id] = true;
                h.id = id;
            }

            var item = document.createElement('li');
            item.className = 'md-toc-' + h.tagName.toLowerCase();

            var link = document.createElement('a');
            link.href = '#' + h.id;
            link.textContent = h.textContent;
            link.addEventListener('click', function (e) {
                e.preventDefault();
                h.scrollIntoView({ behavior: 'smooth', block: 'start' });
                panel.hidden = true;
            });

            item.appendChild(link);
            list.appendChild(item);
        });

        var toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'md-toc-toggle';
        toggle.setAttribute('aria-label', 'Съдържание');
        toggle.textContent = '☰';

        var panel = document.createElement('nav');
        panel.className = 'md-toc-panel';
        panel.hidden = true;
        panel.appendChild(list);

        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            panel.hidden = !panel.hidden;
        });
        document.addEventListener('click', function (e) {
            if (!panel.hidden && !panel.contains(e.target) && e.target !== toggle) {
                panel.hidden = true;
            }
        });

        container.insertBefore(panel, container.firstChild);
        container.insertBefore(toggle, container.firstChild);
    }

    window.renderMarkdownEmbed = function (containerId, mdPath) {
        var container = document.getElementById(containerId);
        if (!container) return;

        container.classList.add('md-embed');

        fetch(mdPath)
            .then(function (response) {
                if (!response.ok) throw new Error(String(response.status));
                return response.text();
            })
            .then(function (raw) {
                var parsed = parseFrontmatter(raw);
                var body = parsed.body;
                var needsMermaid = MERMAID_RE.test(body);
                var needsMath = MATH_RE.test(body);
                var needsToc = isTruthy(parsed.fields.toc);
                var pending = [];

                if (needsMermaid) {
                    pending.push(loadScriptOnce(LIBS_BASE + 'mermaid.min.js'));
                }
                if (needsMath) {
                    loadStylesheetOnce(LIBS_BASE + 'katex/katex.min.css');
                    pending.push(
                        loadScriptOnce(LIBS_BASE + 'katex/katex.min.js')
                            .then(function () { return loadScriptOnce(LIBS_BASE + 'katex/auto-render.min.js'); })
                    );
                }

                return Promise.all(pending).then(function () {
                    container.innerHTML = marked.parse(body);
                    if (needsMermaid) renderMermaid(container);
                    if (needsMath) renderMath(container);
                    if (needsToc) setupToc(container);
                });
            })
            .catch(function () {
                container.textContent = 'Грешка при зареждане на ' + mdPath;
            });
    };
})();
