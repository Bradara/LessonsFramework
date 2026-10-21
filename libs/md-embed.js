/**
 * md-embed.js — вгражда съдържанието на .md файл вътре в урок.
 * Собствен (не CDN-вендорван) helper — изисква marked.js да е зареден преди него.
 *
 * Mermaid диаграми (```mermaid code block) и LaTeX формули ($..$ / $$..$$) се
 * засичат автоматично в текста и mermaid.js/KaTeX се зареждат мързеливо от
 * libs/ само когато реално има такова съдържание - няма нужда от допълнителни
 * <script> тагове в урока за това.
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
                var body = raw.replace(/^---\s*\n[\s\S]*?\n---\s*\n?/, '');
                var needsMermaid = MERMAID_RE.test(body);
                var needsMath = MATH_RE.test(body);
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
                });
            })
            .catch(function () {
                container.textContent = 'Грешка при зареждане на ' + mdPath;
            });
    };
})();
