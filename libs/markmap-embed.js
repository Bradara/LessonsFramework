/**
 * markmap-embed.js — рендира ```mermaid mindmap``` блок от .md файл като
 * интерактивна, пан/зуум + click-to-expand/collapse мисловна карта (markmap),
 * вместо статичното SVG, което рисува mermaid.js за mindmap диаграми.
 *
 * mermaid.js няма вградена интерактивност за mindmap (веднъж нарисуван, SVG-то
 * е статично) - затова не разширяваме md-embed.js, а паралелно рендираме
 * СЪЩИЯ mermaid-синтаксис през markmap-view (libs/markmap/). Самият .md файл
 * не се променя - mermaid синтаксисът се парсва тук директно в дърво
 * {content, children}, без да минава през markdown-it/markmap-lib.
 *
 * Собствен (не CDN-вендорван) helper, както md-embed.js.
 *
 * Употреба:
 *   <link rel="stylesheet" href="../../../libs/markmap-embed.css">
 *   ...
 *   <div class="markmap-host">
 *       <svg id="my-mindmap"></svg>
 *       <div class="markmap-toolbar-host"></div>
 *   </div>
 *   <script src="../../../libs/markmap-embed.js"></script>
 *   <script>
 *       document.addEventListener('DOMContentLoaded', function () {
 *           renderMermaidMindmap('my-mindmap', 'мисловна-карта.md');
 *       });
 *   </script>
 *
 * ВАЖНО: контейнерът (.markmap-host) трябва да е видим (display:block) в
 * момента на извикване - markmap-view измерва размера на SVG-то при fit(),
 * точно както H5P и mermaid.run() в md-embed.js. В таб-базирани уроци викай
 * renderMermaidMindmap() лениво, след showTab() е сложил класа "active".
 */
(function () {
    var LIBS_BASE = (document.currentScript && document.currentScript.src)
        ? document.currentScript.src.replace(/markmap-embed\.js(?:\?.*)?$/, '')
        : '';

    var FRONTMATTER_RE = /^---\s*\n[\s\S]*?\n---\s*\n?/;
    var MERMAID_BLOCK_RE = /```mermaid\s*\n([\s\S]*?)```/;

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

    function escapeHtml(text) {
        return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // Маха mermaid "формата" на възела (id((текст)), id[текст], id{{текст}}, id(текст))
    // и ::icon()/:::class анотациите, за да остане само видимият текст.
    function stripMermaidNodeShape(raw) {
        var text = raw.replace(/:::\S+\s*$/, '').replace(/::icon\([^)]*\)/, '').trim();
        var shapes = [
            /^[A-Za-z0-9_-]*\(\(([\s\S]*)\)\)$/,  // ((кръг))
            /^[A-Za-z0-9_-]*\{\{([\s\S]*)\}\}$/,  // {{шестоъгълник}}
            /^[A-Za-z0-9_-]*\[([\s\S]*)\]$/,      // [квадрат]
            /^[A-Za-z0-9_-]*\(([\s\S]*)\)$/       // (заоблен правоъгълник)
        ];
        for (var i = 0; i < shapes.length; i++) {
            var m = text.match(shapes[i]);
            if (m) return m[1].trim();
        }
        return text;
    }

    // Превръща текста на mermaid "mindmap" блока в дърво {content, children} -
    // форматът, който markmap-view очаква. Йерархията се определя по отстъпа
    // (брой водещи интервали спрямо предходните редове), без да се предполага
    // фиксирана стъпка от 2 интервала.
    function parseMermaidMindmap(block) {
        var stack = []; // { indent, node }
        var root = null;
        var started = false;

        block.split('\n').forEach(function (raw) {
            if (!raw.trim()) return;
            var indent = raw.match(/^(\s*)/)[1].length;
            var text = raw.trim();

            if (!started) {
                if (text === 'mindmap') started = true;
                return;
            }

            var node = { content: escapeHtml(stripMermaidNodeShape(text)), children: [] };

            if (!root) {
                root = node;
                stack.push({ indent: indent, node: node });
                return;
            }

            while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
            var parent = stack.length ? stack[stack.length - 1].node : root;
            parent.children.push(node);
            stack.push({ indent: indent, node: node });
        });

        return root;
    }

    window.renderMermaidMindmap = function (svgId, mdPath, options) {
        var svgEl = document.getElementById(svgId);
        if (!svgEl) return;

        fetch(mdPath)
            .then(function (response) {
                if (!response.ok) throw new Error(String(response.status));
                return response.text();
            })
            .then(function (raw) {
                var body = raw.replace(FRONTMATTER_RE, '');
                var match = body.match(MERMAID_BLOCK_RE);
                if (!match) throw new Error('не е открит ```mermaid блок в ' + mdPath);
                var tree = parseMermaidMindmap(match[1]);
                if (!tree) throw new Error('празна мисловна карта в ' + mdPath);

                return loadScriptOnce(LIBS_BASE + 'markmap/d3.min.js')
                    .then(function () { return loadScriptOnce(LIBS_BASE + 'markmap/markmap-view.min.js'); })
                    .then(function () {
                        loadStylesheetOnce(LIBS_BASE + 'markmap/markmap-toolbar.css');
                        return loadScriptOnce(LIBS_BASE + 'markmap/markmap-toolbar.min.js');
                    })
                    .then(function () {
                        var mm = window.markmap.Markmap.create(svgEl, Object.assign({
                            initialExpandLevel: 2,
                            duration: 400,
                            maxWidth: 260,
                            autoFit: true
                        }, options), tree);

                        var toolbarHost = svgEl.parentElement && svgEl.parentElement.querySelector('.markmap-toolbar-host');
                        if (toolbarHost && window.markmap.Toolbar) {
                            var toolbar = window.markmap.Toolbar.create(mm);
                            toolbar.showBrand = false;
                            toolbar.setItems(['zoomIn', 'zoomOut', 'fit']);
                            toolbarHost.appendChild(toolbar.el);
                        }

                        window.addEventListener('resize', function () { mm.fit(); });
                        return mm;
                    });
            })
            .catch(function (err) {
                svgEl.outerHTML = '<p class="markmap-error">Грешка при зареждане на мисловната карта: ' + err.message + '</p>';
            });
    };
})();
