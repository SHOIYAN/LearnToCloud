import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './App.module.css';

const API_BASE_URL = 'http://localhost:8000';

// Component for displaying a list of albums
const AlbumList = ({ albums, selectedGenre, selectedYear }) => {
  const filteredAlbums = albums.filter((album) => {
    const matchesGenre = selectedGenre ? album.genre === selectedGenre : true;
    const matchesYear = selectedYear ? album.releaseYear === selectedYear : true;
    return matchesGenre && matchesYear;
  });

  return (
    <div className={styles.albumList}>
      <h2>Albums</h2>
      {filteredAlbums.length === 0 ? (
        <p>No albums found for the selected Release Year.</p>
      ) : (
        <ul>
          {filteredAlbums.map((album) => (
            <li key={album.album_id} className={styles.album}>
              <h3>{album.title}</h3>
              <p>Artist: {album.artist}</p>
              <p>Genre: {album.genre}</p>
              <p>Release Year: {album.releaseYear}</p>
              <img
                src={album.coverUrl}
                alt={`Cover of ${album.title}`}
                className={styles.coverImage}
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

// Component for displaying genres and release year dropdown
const Sidebar = ({ genres, years, selectedGenre, selectedYear, onGenreSelect, onYearSelect }) => {
  return (
    <div className={styles.genreList}>
      <h2>Genres</h2>
      <ul>
        {genres.map((genre) => (
          <li
            key={genre}
            className={`${styles.genreItem} ${
              genre === selectedGenre ? styles.selectedGenre : ''
            }`}
            onClick={() => onGenreSelect(genre)}
          >
            {genre}
          </li>
        ))}
      </ul>
      <div className={styles.yearFilter}>
        <h3>Release Year</h3>
        <select
          value={selectedYear || ''}
          onChange={(e) => onYearSelect(e.target.value)}
        >
          <option value="">All Years</option>
          {years.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

// Main App component
const App = () => {
  const [genres, setGenres] = useState([]);
  const [years, setYears] = useState([]);
  const [albums, setAlbums] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState(null);
  const [selectedYear, setSelectedYear] = useState(null);

  useEffect(() => {
    // Fetch albums from the API
    const fetchAlbums = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/getalbums`);
        setAlbums(response.data);
        // Extract unique genres and years from the albums
        const uniqueGenres = [...new Set(response.data.map((album) => album.genre))];
        const uniqueYears = [...new Set(response.data.map((album) => album.releaseYear))].sort();
        setGenres(uniqueGenres);
        setYears(uniqueYears);
      } catch (error) {
        console.error('Error fetching albums:', error);
      }
    };

    fetchAlbums();
  }, []);

  return (
    <div className={styles.app}>
      <h1 className={styles.header}>Music Albums</h1>
      <div className={styles.container}>
        {/* Sidebar for genres and year filter */}
        <Sidebar
          genres={genres}
          years={years}
          selectedGenre={selectedGenre}
          selectedYear={selectedYear}
          onGenreSelect={(genre) => {
            setSelectedGenre(genre);
            setSelectedYear(null); // Reset year when genre is selected
          }}
          onYearSelect={(year) => setSelectedYear(year || null)}
        />
        {/* Albums list */}
        <AlbumList albums={albums} selectedGenre={selectedGenre} selectedYear={selectedYear} />
      </div>
    </div>
  );
};

export default App;
