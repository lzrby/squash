import React from 'react';
import './App.scss';
import data from './rating.json';

const { PUBLIC_URL } = process.env;

const Player = ({ name, rating }) => (
  <div className="list__person">
    <img
      className="person__image"
      src={`${PUBLIC_URL}/avatars/${name}.jpg`}
      alt={name}
    />
    <p className="person__name">{name}</p>
    <p className="person__rating">{rating}</p>
  </div>
);

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
