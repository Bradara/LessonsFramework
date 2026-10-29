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
 * Поддържа два варианта на .md файла:
 *   1. ```mermaid mindmap``` код блок вътре в markdown текст (напр. статия).
 *   2. "Суров" mermaid source, както се копира директно от mermaid.live -
 *      незадължителен YAML frontmatter с mermaid-специфичен config/theme,
 *      последван директно от "mindmap" без ``` ограждане. Frontmatter-ът се
 *      маха и игнорира (markmap-view си има собствено оцветяване/layout) -
 *      само структурата на възлите се чете от него.
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
 *
 * Бутон "Цял екран": автоматично се добавя в .markmap-toolbar-host до
 * zoom/fit бутоните. Пробва Fullscreen API (host.requestFullscreen()); ако
 * браузърът го откаже - типично защото урокът е вграден в <iframe> без
 * allow="fullscreen" (Moodle Book ресурс - вижда се само URL-ът, не и
 * iframe тагът, затова не може да се сложи това разрешение) - пада назад
 * към CSS клас .markmap-pseudo-fullscreen, който прави .markmap-host
 * position:fixed и запълва viewport-а на самия документ/iframe (не целия
 * екран). Изход: бутонът пак, или Escape в псевдо-режим.
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

    // Маха едни единствени ограждащи кавички ("текст" -> текст) - mermaid
    // позволява текстът вътре във всяка форма да е квотиран, за да съдържа
    // специални знаци.
    function stripWrappingQuotes(text) {
        if (text.length >= 2 && text[0] === '"' && text[text.length - 1] === '"') {
            return text.slice(1, -1).trim();
        }
        return text;
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
            if (m) return stripWrappingQuotes(m[1].trim());
        }
        return stripWrappingQuotes(text);
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

    // Взима mermaid mindmap source-а от .md файла - или от ```mermaid код блок,
    // или (ако няма такъв) от целия текст след frontmatter-а, стига да съдържа
    // декларацията "mindmap" (суров mermaid.live export).
    function extractMermaidSource(raw) {
        var body = raw.replace(FRONTMATTER_RE, '');
        var fenced = body.match(MERMAID_BLOCK_RE);
        if (fenced) return fenced[1];
        if (/(^|\n)\s*mindmap\s*(\n|$)/.test(body)) return body;
        return null;
    }

    function requestFs(el) {
        var fn = el.requestFullscreen || el.webkitRequestFullscreen;
        return fn ? fn.call(el) : Promise.reject(new Error('Fullscreen API не се поддържа'));
    }

    function exitFs() {
        var fn = document.exitFullscreen || document.webkitExitFullscreen;
        return fn ? fn.call(document) : Promise.resolve();
    }

    function fsElement() {
        return document.fullscreenElement || document.webkitFullscreenElement;
    }

    // Добавя бутон "Цял екран" до zoom toolbar-а. Пробва истинския Fullscreen
    // API (работи при пряко отваряне на урока, или ако родителската страница
    // е сложила allow="fullscreen" на <iframe>-а); ако браузърът го откаже -
    // типично когато урокът е вграден без това разрешение, какъвто е случаят
    // с Moodle Book ресурс, където не контролираш iframe тага - превключва
    // на CSS fallback (.markmap-pseudo-fullscreen), който запълва целия
    // видим viewport на самия документ/iframe вместо целия екран.
    function setupFullscreenButton(host, mm, toolbarHost) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'markmap-fullscreen-btn';

        function active() {
            return host.classList.contains('markmap-pseudo-fullscreen') || fsElement() === host;
        }

        function refresh() {
            btn.innerHTML = active() ? '<i class="fas fa-compress"></i>' : '<i class="fas fa-expand"></i>';
            btn.title = active() ? 'Изход от цял екран' : 'Цял екран';
        }

        function afterToggle() {
            refresh();
            window.dispatchEvent(new Event('resize'));
            requestAnimationFrame(function () { mm.fit(); });
        }

        function onKeydown(e) {
            if (e.key === 'Escape' && host.classList.contains('markmap-pseudo-fullscreen')) {
                exitPseudo();
            }
        }

        function enterPseudo() {
            host.classList.add('markmap-pseudo-fullscreen');
            document.addEventListener('keydown', onKeydown);
            afterToggle();
        }

        function exitPseudo() {
            host.classList.remove('markmap-pseudo-fullscreen');
            document.removeEventListener('keydown', onKeydown);
            afterToggle();
        }

        btn.addEventListener('click', function () {
            if (host.classList.contains('markmap-pseudo-fullscreen')) {
                exitPseudo();
                return;
            }
            if (fsElement() === host) {
                exitFs().catch(function () {});
                return;
            }
            requestFs(host).catch(function () { enterPseudo(); });
        });

        document.addEventListener('fullscreenchange', afterToggle);
        document.addEventListener('webkitfullscreenchange', afterToggle);

        refresh();
        toolbarHost.appendChild(btn);
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
                var source = extractMermaidSource(raw);
                if (source === null) throw new Error('не е открит mermaid mindmap в ' + mdPath);
                var tree = parseMermaidMindmap(source);
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

                        var host = svgEl.parentElement;
                        var toolbarHost = host && host.querySelector('.markmap-toolbar-host');
                        if (toolbarHost && window.markmap.Toolbar) {
                            var toolbar = window.markmap.Toolbar.create(mm);
                            toolbar.showBrand = false;
                            toolbar.setItems(['zoomIn', 'zoomOut', 'fit']);
                            toolbarHost.appendChild(toolbar.el);
                        }
                        if (toolbarHost && host) {
                            setupFullscreenButton(host, mm, toolbarHost);
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
