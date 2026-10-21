/**
 * md-embed.js — вгражда съдържанието на .md файл вътре в урок.
 * Собствен (не CDN-вендорван) helper — изисква marked.js да е зареден преди него.
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
function renderMarkdownEmbed(containerId, mdPath) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.classList.add('md-embed');
    fetch(mdPath)
        .then(function (response) {
            if (!response.ok) throw new Error(response.status);
            return response.text();
        })
        .then(function (raw) {
            const body = raw.replace(/^---\s*\n[\s\S]*?\n---\s*\n?/, '');
            container.innerHTML = marked.parse(body);
        })
        .catch(function () {
            container.textContent = 'Грешка при зареждане на ' + mdPath;
        });
}
