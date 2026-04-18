import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <main className="app-container">
      <h1>ADK Frontend POC</h1>
      <p className="subtitle">This simple home page links to each agent UI route as they are added.</p>

      <section className="home-links" aria-label="Available pages">
        <h2>Available pages</h2>
        <ul>
          <li>
            <Link to="/fun-facts">Fun Facts Explorer</Link>
          </li>
        </ul>
      </section>
    </main>
  );
}

export default HomePage;
