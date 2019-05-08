import React from 'react';
import './App.scss';
import data from './raiting.json';
import { DEFAULT_AVATAR, CUP_LOGO } from './constants';

const Player = ({ name, image, rating }) => (
  <div className="list__person">
    <img className="person__image" src={image} alt={name} />
    <p className="person__name">{name}</p>
    <p className="person__rating">{rating}</p>
  </div>
);

Player.defaultProps = {
  image: DEFAULT_AVATAR,
};

const Header = () => (
  <div className="header">
    <img className="header__icon" src={CUP_LOGO} alt="logo" />
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
