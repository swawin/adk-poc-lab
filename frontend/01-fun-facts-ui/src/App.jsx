import { useState } from 'react';
import { BACKEND_BASE_URL } from './config';

function App() {
  const [topic, setTopic] = useState('space');
  const [facts, setFacts] = useState([]);
  const [resultTopic, setResultTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const getFunFacts = async () => {
    const trimmedTopic = topic.trim();

    if (!trimmedTopic) {
      setError('Please enter a topic to fetch fun facts.');
      setFacts([]);
      setResultTopic('');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const params = new URLSearchParams({ topic: trimmedTopic });
      const response = await fetch(`${BACKEND_BASE_URL}/fun-fact?${params.toString()}`);

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setFacts(Array.isArray(data.facts) ? data.facts : []);
      setResultTopic(data.topic || trimmedTopic);
    } catch (err) {
      setFacts([]);
      setResultTopic('');
      setError('Sorry, something went wrong while fetching fun facts. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-container">
      <h1>Fun Facts Explorer</h1>
      <p className="subtitle">Ask the ADK backend for a topic and get 5 fun facts.</p>

      <section className="controls" aria-label="Fun facts request form">
        <label htmlFor="topic-input">Topic</label>
        <input
          id="topic-input"
          type="text"
          value={topic}
          onChange={(event) => setTopic(event.target.value)}
          placeholder="Try: space, oceans, dinosaurs"
        />
        <button type="button" onClick={getFunFacts} disabled={loading}>
          {loading ? 'Loading...' : 'Get Fun Facts'}
        </button>
      </section>

      {error && <p className="message error">{error}</p>}

      {facts.length > 0 && (
        <section className="results" aria-live="polite">
          <h2>5 fun facts about "{resultTopic}"</h2>
          <ol>
            {facts.map((fact, index) => (
              <li key={`${fact}-${index}`}>{fact}</li>
            ))}
          </ol>
        </section>
      )}
    </main>
  );
}

export default App;
