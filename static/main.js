let rendererCode = '';
const {createApp} = Vue

createApp({
    data() {
        return {
            titleLines: [['Reduction Mammoplasty Risk Profile', '#000000']],
            ticks: '15%, 30%, 45%',
            bars: [{
                'label': 'Common risk (50%)',
                'color': 'green',
                'severity': 'moderate',
                'value': 50,
            }, {
                'label': 'Nipple Complication (9%)',
                'color': 'red',
                'severity': 'moderate',
                'value': 9,
            }, {
                'label': 'Donor Site Uncomplicated Healing (30%)',
                'color': 'green',
                'severity': 'significant',
                'value': 40,
            }, {
                'label': 'Lifetime Risk of Skin Cancer In Australia (66%)',
                'color': 'grey',
                'severity': 'moderate',
                'value': 66,
            }, {
                'label': 'Risk of Sports Related ER Visit (50%)',
                'color': 'red',
                'severity': 'moderate',
                'value': 50,
            }],
            severityConverter: {
                'mild': 0,
                'minor': 0.25,
                'moderate': 0.5,
                'significant': 0.75,
                'severe': 1
            },
            draw_arrows: false,
            rendering: false
        }
    }, methods: {
        addTitleLine(evt) {
            evt.preventDefault();
            this.titleLines.push(['New line', '#000000']);
        },
        removeTitleLine(evt, index) {
            evt.preventDefault();
            if (index < this.titleLines.length) {
                this.titleLines.splice(index, 1);
            }
        }, rand(min, max) {
            min = Math.ceil(min);
            max = Math.floor(max);
            return Math.floor(Math.random() * (max - min) + min);
        },
        addBar(evt) {
            evt.preventDefault();
            let colors = ['green', 'red', 'grey'];
            let severities = ['mild', 'minor', 'moderate', 'significant', 'severe'];
            this.bars.push({
                'label': 'New label',
                'color': colors[this.rand(0, 3)],
                'severity': severities[this.rand(0, 5)],
                'value': this.rand(1, 50),
            });
        },
        removeBar(evt, index) {
            evt.preventDefault();
            if (index < this.bars.length) {
                this.bars.splice(index, 1);
            }
        },
        parseTicks() {
            let ticks = [];
            for (const part of this.ticks.split(',')) {
                const pct = parseInt(part.trim().replace('%'));
                if (!isNaN(pct)) {
                    ticks.push(pct / 100);
                }
            }
            return ticks;
        },
        render() {
            let self = this;
            this.rendering = true;
            for (let child of document.getElementById('root').children) {
                if (child.id.startsWith('matplotlib_')) {
                    child.remove();
                }
            }
            pyodide.globals.set('plot_args', JSON.stringify({
                title: this.titleLines,
                ticks: this.parseTicks(),
                bars: this.bars.map(b => Object.assign({}, b, {
                    value: b.value / 100,
                    color_value: this.severityConverter[b.severity]
                })),
                draw_arrows: this.draw_arrows
            }));
            pyodide.runPythonAsync(`
                import json
                from plasticsplot import plotter
                plotter.main(json.loads(plot_args))
                `).finally(() => {
                self.rendering = false;
            });
        }
    }
}).mount('#app');

async function load() {
    Promise.all([
        loadPyodide().then((pyodide) => {
            window.pyodide = pyodide;
            return pyodide.loadPackage(['micropip', 'matplotlib']);
        }).then(() =>
            pyodide.runPythonAsync(`
                import micropip
                await micropip.install('./dist/plasticsplot-0.0.1-py3-none-any.whl')
                import matplotlib
                matplotlib.use('module://matplotlib.backends.html5_canvas_backend')`)
        )
    ]).then(res => {
        document.getElementById('loading-wrapper').classList.add('is-hidden');
        document.getElementById('content').classList.remove('is-hidden');
        rendererCode = res[1];
    });
}

load();