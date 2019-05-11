import React from 'react';
import './App.scss';
import data from './rating.json';

import DeltaArrow from './components/DeltaArrow';

const { PUBLIC_URL } = process.env;

const Player = ({ name, rating, sets, prev_rating }) => {
  const delta = rating - prev_rating;

  return (
    <div className="list__person">
      <img
        className="person__image"
        src={`${PUBLIC_URL}/avatars/${name}.jpg`}
        alt={name}
      />
      <p className="person__name">{name}</p>
      <div className="person__rating">
        <span className="person__rating-value">{rating}</span>
        <div className="person__rating-stats">
          <DeltaArrow value={delta} />{' '}
          <span className="person__sets">({sets})</span>
        </div>
      </div>
    </div>
  );
};

const Header = () => (
  <div className="header">
    <img className="header__icon" src={`${PUBLIC_URL}/cup.png`} alt="logo" />
    <h1 className="header__title">
      Squash
      <span>Leaderboard</span>
    </h1>
  </div>
);

const App = () => (
  <div className="app">
    <Header />
    <div className="list">
      {data.map(player => (
        <Player key={player.name} {...player} />
      ))}
    </div>
  </div>
);

export default App;
