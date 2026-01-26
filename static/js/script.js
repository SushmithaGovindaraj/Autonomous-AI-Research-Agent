document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const input = document.getElementById('research-input');
    const startBtn = document.getElementById('start-btn');
    const statusDisplay = document.getElementById('status-display');
    const statusText = document.getElementById('status-text');
    const consoleLogs = document.getElementById('console-logs');
    const resultsSection = document.getElementById('results-section');
    const reportContent = document.getElementById('report-content');
    const chartContainer = document.getElementById('chart-container');
    const sourcesList = document.getElementById('sources-list');
    const filesList = document.getElementById('files-list');

    // Suggestion chips
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            input.value = chip.textContent;
            input.focus();
        });
    });

    // Start Research
    const startResearch = async () => {
        const task = input.value.trim();
        if (!task) return;

        // Reset UI
        resultsSection.classList.add('hidden');
        statusDisplay.classList.remove('hidden');
        consoleLogs.innerHTML = '';
        chartContainer.innerHTML = '';
        sourcesList.innerHTML = '';
        filesList.innerHTML = '';

        // Reset steps
        document.querySelectorAll('.step').forEach(s => {
            s.classList.remove('active', 'done');
        });

        // Disable input
        input.disabled = true;
        startBtn.disabled = true;
        startBtn.textContent = 'Researching...';

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
                        const jsonStr = line.slice(6);
                        if (!jsonStr.trim()) continue;

                        try {
                            const data = JSON.parse(jsonStr);
                            handleUpdate(data);
                        } catch (e) {
                            console.error('Error parsing JSON:', e);
                        }
                    }
                }
            }
        } catch (err) {
            console.error('Error starting research:', err);
            logToConsole(`Error: ${err.message}`);
        } finally {
            input.disabled = false;
            startBtn.disabled = false;
            startBtn.textContent = 'Start Research';
        }
    };

    startBtn.addEventListener('click', startResearch);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') startResearch();
    });

    // Handle updates from server
    function handleUpdate(data) {
        if (data.status === 'complete') {
            statusText.textContent = 'Research Complete';
            document.querySelector('.spinner').style.display = 'none';
            return;
        }

        if (data.error) {
            logToConsole(`❌ Error: ${data.error}`);
            statusText.textContent = 'Error occurred';
            return;
        }

        // Update steps
        if (data.node) {
            updateStep(data.node);
            logToConsole(`🔄 ${data.node.toUpperCase()}: ${data.current_step || 'Working...'}`);
        }

        // Update Report (Markdown)
        if (data.report) {
            resultsSection.classList.remove('hidden');
            reportContent.innerHTML = marked.parse(data.report);
        }

        // Update Files/Charts
        if (data.files && data.files.length > 0) {
            updateFiles(data.files);
        }

        // Update Sources
        if (data.sources && data.sources.length > 0) {
            updateSources(data.sources);
        }
    }

    function updateStep(nodeName) {
        document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));

        const stepId = `step-${nodeName}`;
        const stepEl = document.getElementById(stepId);
        if (stepEl) {
            stepEl.classList.add('active');
            // Mark previous steps as done - heuristic
            if (nodeName === 'researcher') document.getElementById('step-planner').classList.add('done');
            if (nodeName === 'coder') {
                document.getElementById('step-planner').classList.add('done');
                document.getElementById('step-researcher').classList.add('done');
            }
            if (nodeName === 'evaluator') {
                document.getElementById('step-planner').classList.add('done');
                document.getElementById('step-researcher').classList.add('done');
                document.getElementById('step-coder').classList.add('done');
            }
        }
    }

    function logToConsole(text) {
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.textContent = `> ${text}`;
        consoleLogs.appendChild(div);
        consoleLogs.scrollTop = consoleLogs.scrollHeight;
    }

    function updateFiles(files) {
        chartContainer.innerHTML = '';
        filesList.innerHTML = '';

        files.forEach(file => {
            const fileName = file.split('/').pop();
            const cleanName = fileName.replace(/_/g, ' ').replace(/\.csv|\.png/, '');

            // Assume files are served from /outputs/filename
            // Note: The backend passes full paths like research_outputs/dataset.csv
            // We need to serve them. The backend mounts 'outputs' to research_outputs.
            const url = `/outputs/${fileName}`;

            if (fileName.endsWith('.png')) {
                const img = document.createElement('img');
                img.src = url;
                img.alt = cleanName;
                chartContainer.appendChild(img);
            } else {
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                a.textContent = `📄 Download ${cleanName} (${fileName.split('.').pop().toUpperCase()})`;
                filesList.appendChild(a);
            }
        });
    }

    function updateSources(sources) {
        sourcesList.innerHTML = '';
        sources.forEach(source => {
            const div = document.createElement('div');
            div.className = 'files-list'; // reusing style
            const a = document.createElement('a');
            a.href = source;
            a.target = '_blank';
            a.textContent = `🔗 ${new URL(source).hostname}`;
            div.appendChild(a);
            sourcesList.appendChild(div);
        });
    }
});
