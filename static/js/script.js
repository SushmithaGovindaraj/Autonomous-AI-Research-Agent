document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const input = document.getElementById('research-input');
    const startBtn = document.getElementById('start-btn');
    const statusSection = document.getElementById('status-section');
    const resultsSection = document.getElementById('results-section');
    const consoleLogs = document.getElementById('console-logs');
    const currentPhase = document.getElementById('current-phase');
    const currentAction = document.getElementById('current-action');
    const reportContent = document.getElementById('report-content');

    // --- Suggestions ---
    window.useSuggestion = (text) => {
        input.value = text;
        startResearch();
    };

    // --- Core Logic ---
    const startResearch = async () => {
        const task = input.value.trim();
        if (!task) return;

        // UI Transition
        document.querySelector('.hero').style.display = 'none';
        document.querySelector('.search-interface').style.display = 'none';
        statusSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        // Reset
        consoleLogs.innerHTML = '';
        currentPhase.textContent = 'Initializing Agent Protocol...';

        try {
            const response = await fetch('/api/research/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            handleUpdate(data);
                        } catch (e) { }
                    }
                }
            }
        } catch (error) {
            log(`CRITICAL ERROR: ${error.message}`, 'red');
        }
    };

    // --- Event Listeners ---
    startBtn.addEventListener('click', startResearch);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') startResearch();
    });

    // --- UI Update Logic ---
    function handleUpdate(data) {
        if (data.status === 'complete') {
            finishResearch();
            return;
        }

        if (data.node) {
            // Update Phase Title
            currentPhase.textContent = `Phase: ${data.node.toUpperCase()}`;
            highlightStep(data.node);

            // Log logic
            const msgs = {
                'planner': 'Analyzing request & formulating strategy...',
                'researcher': 'Scouring the web for relevant data...',
                'coder': 'Generating data visualization scripts...',
                'evaluator': 'Synthesizing final comprehensive report...'
            };
            currentAction.textContent = msgs[data.node] || 'Processing...';
            log(`[${data.node.toUpperCase()}] Executing...`);
        }

        // Live Report Preview
        if (data.report) {
            reportContent.innerHTML = marked.parse(data.report);
            // Show results section early if we have a report, for live viewing
            resultsSection.classList.remove('hidden');
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }

        if (data.files && data.files.length) updateAssets(data.files);
        if (data.sources && data.sources.length) updateSources(data.sources);
    }

    function highlightStep(step) {
        document.querySelectorAll('.step-item').forEach(s => s.classList.remove('active'));
        const el = document.getElementById(`step-${step}`);
        if (el) el.classList.add('active');
    }

    function log(text, color = 'white') {
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.innerHTML = `<span style="color: #6366f1;">$</span> ${text}`;
        if (color === 'red') div.style.color = '#ef4444';
        consoleLogs.appendChild(div);
        consoleLogs.scrollTop = consoleLogs.scrollHeight;
    }

    function updateAssets(files) {
        const container = document.getElementById('chart-container');
        const list = document.getElementById('files-list');
        container.innerHTML = '';
        list.innerHTML = '';

        files.forEach(f => {
            const name = f.split('/').pop();
            const url = `/outputs/${name}`;

            if (name.endsWith('.png')) {
                const img = document.createElement('img');
                img.src = url;
                container.appendChild(img);
            } else {
                const a = document.createElement('a');
                a.href = url;
                a.innerHTML = `<i class="ri-file-text-line"></i> ${name}`;
                list.appendChild(a);
            }
        });
    }

    function updateSources(sources) {
        const list = document.getElementById('sources-list');
        list.innerHTML = '';
        sources.forEach(s => {
            const a = document.createElement('a');
            a.href = s;
            a.target = '_blank';
            a.innerHTML = `<i class="ri-link"></i> ${new URL(s).hostname}`;
            list.appendChild(a);
        });
    }

    function finishResearch() {
        statusSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        document.querySelector('.hero').style.display = 'none';
        currentPhase.textContent = 'Mission Complete';
        // Check for PDF export capability
    }

    // --- PDF Export (Placeholder) ---
    window.exportPDF = () => {
        window.print();
    };
});
