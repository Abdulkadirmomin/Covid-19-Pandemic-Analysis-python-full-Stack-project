const e = React.createElement;
const {useState, useEffect} = React;

function App() {
  const [summary, setSummary] = useState([]);
  const [country, setCountry] = useState('');
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/summary')
      .then(r => r.json())
      .then(setSummary)
      .catch(e => console.error(e));
  }, []);

  function loadCountry() {
    const q = country ? '?country=' + encodeURIComponent(country) : '';
    fetch('/api/data' + q)
      .then(r => r.json())
      .then(setData)
      .catch(e => console.error(e));
  }

  return e('div', {style:{fontFamily:'Arial', padding:20}},
    e('h1', null, 'COVID-19 Analysis (Sample)'),
    e('p', null, 'This is a small demo frontend that queries the Flask backend.'),
    e('h2', null, 'Summary by Country'),
    e('ul', null, summary.map(s => e('li', {key:s.country}, `${s.country}: confirmed=${s.confirmed}, deaths=${s.deaths}, recovered=${s.recovered}`))),
    e('hr', null),
    e('div', null,
      e('input', {placeholder:'Country (e.g. India)', value:country, onChange: (ev)=>setCountry(ev.target.value)}),
      e('button', {onClick: loadCountry, style:{marginLeft:8}}, 'Load Data')
    ),
    e('h3', null, 'Data Rows'),
    e('table', {border:1, cellPadding:6},
      e('thead', null, e('tr', null, ['date','country','confirmed','deaths','recovered'].map(h => e('th', {key:h}, h)))),
      e('tbody', null, data.map((row, idx) => e('tr', {key:idx}, [
        e('td', {key:1}, row.date),
        e('td', {key:2}, row.country),
        e('td', {key:3}, row.confirmed),
        e('td', {key:4}, row.deaths),
        e('td', {key:5}, row.recovered),
      ])))
    )
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
