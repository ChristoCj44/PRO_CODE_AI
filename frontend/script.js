// Initialize Monaco Editor
require.config({
    paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.36.1/min/vs' }
});

let editor;

require(['vs/editor/editor.main'], function () {

    // 🎨 Custom VS Code style theme
    monaco.editor.defineTheme('algomindml-dark', {
        base: 'vs-dark',
        inherit: true,

        rules: [
            { token: 'keyword', foreground: 'C586C0' },     // def, for, if
            { token: 'string', foreground: 'CE9178' },      // "Hello"
            { token: 'number', foreground: 'B5CEA8' },      // 123
            { token: 'comment', foreground: '6A9955' },     // # comments
            { token: 'identifier', foreground: '9CDCFE' }  // variables
        ],

        colors: {
            'editor.background': '#1e1e1e',
            'editor.foreground': '#d4d4d4',
            'editorCursor.foreground': '#ffffff',
            'editor.selectionBackground': '#264f78',
            'editor.lineHighlightBackground': '#2a2a2a'
        }
    });

    // 🧠 Create editor using custom theme
    editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: '# Welcome to AlgoMindML\n\ndef main():\n    print("Hello, World!")\n    \n    # Example: Inefficient loop for AI analysis\n    data = [1, 2, 3, 4, 5]\n    for i in data:\n        for j in data:\n            print(i, j)\n\nmain()',

        language: 'python',
        theme: 'algomindml-dark',
        automaticLayout: true,
        fontSize: 14,
        minimap: { enabled: false },

        // ✨ VS Code feel improvements
        cursorBlinking: 'smooth',
        smoothScrolling: true,
        bracketPairColorization: { enabled: true },
        guides: { bracketPairs: true },
        autoIndent: 'full',
        formatOnPaste: true,
        formatOnType: true
    });

});


// ===============================
// Run Code Function (UNCHANGED)
// ===============================

async function runCode() {
    const runBtn = document.getElementById('run-btn');
    const outputConsole = document.getElementById('output-console');
    const badge = document.getElementById('status-badge');

    // UI State -> Loading
    runBtn.disabled = true;
    runBtn.innerHTML = '<span class="icon">⏳</span> Analyzing...';
    badge.textContent = "Processing";
    badge.style.background = "#e6a23c";
    outputConsole.textContent = 'Executing & Analyzing...';

    const code = editor.getValue();

    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language: 'python', code })
        });

        const result = await response.json();

        if (result.error) {
            outputConsole.innerHTML = `<span class="error-text">${result.error}</span>`;
            badge.textContent = "Error";
            badge.style.background = "var(--error)";
        } else {
            outputConsole.innerHTML = `<span class="success-text">${result.output}</span>`;
            badge.textContent = `Success (${result.execution_time})`;
            badge.style.background = "var(--success)";
        }

        // AI Complexity Results


    } catch (err) {
        outputConsole.innerHTML = `<span class="error-text">Network Error: ${err.message}</span>`;
        badge.textContent = "Failed";
        badge.style.background = "var(--error)";
    } finally {
        runBtn.disabled = false;
        runBtn.innerHTML = '<span class="icon">▶</span> Run Code';
    }
}

async function analyzeCode() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const badge = document.getElementById('status-badge');

    // UI State -> Loading
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="icon">⏳</span> Analyzing...';

    // Reset previous analysis
    document.getElementById('time-comp').textContent = "--";
    document.getElementById('space-comp').textContent = "--";
    document.getElementById('confidence').textContent = "--";
    document.getElementById('explanation').textContent = "Analyzing complexity...";
    document.getElementById('suggestions').textContent = "--";

    const code = editor.getValue();

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language: 'python', code })
        });

        const result = await response.json();

        if (result.error) {
            document.getElementById('explanation').innerHTML = `<span class="error-text">${result.error}</span>`;
        } else {
            // AI Complexity Results
            document.getElementById('time-comp').textContent = result.complexity.time_complexity;
            document.getElementById('space-comp').textContent = result.complexity.space_complexity;
            document.getElementById('confidence').textContent = result.complexity.confidence;
            document.getElementById('explanation').textContent = result.complexity.explanation;
            document.getElementById('suggestions').textContent =
                result.complexity.suggestions || "No suggestions.";
        }

    } catch (err) {
        document.getElementById('explanation').innerHTML = `<span class="error-text">Network Error: ${err.message}</span>`;
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<span class="icon"></span> AI Analysis';
    }
}
