import React from 'react';
import PropTypes from 'prop-types';
import './App.scss';
import data from './rating.json';

import DeltaArrow from './components/DeltaArrow';
import { colorByPercent } from './utils';

const { PUBLIC_URL } = process.env;

const Player = ({ name, rating, sets, sets_won, prev_rating }) => {
  const delta = rating - prev_rating;
  const winRate = Math.floor((sets_won / sets) * 100);

  return (
    <div className="list__person">
      <img
        className="person__image"
        src={`${PUBLIC_URL}/avatars/${name}.jpg`}
        alt={name}
      />
      <div className="person__row">
        <div className="person__row__name">{name}</div>
        <div className="person__row__sets">
          <span title="sets played">
            <span role="img" aria-labelledby="games">
              🏏
            </span>
            : {sets}
          </span>
          ,{' '}
          <span title="win rate">
            <span role="img" aria-labelledby="win rate">
              🥇
            </span>
            : <span style={{ color: colorByPercent(winRate) }}>{winRate}%</span>
          </span>
        </div>
      </div>

      <div className="person__rating">
        <span className="person__rating-value">{rating}</span>
        <div className="person__rating-delta">
          <DeltaArrow value={delta} />
        </div>
      </div>
    </div>
  );
};

Player.propTypes = {
  name: PropTypes.string.isRequired,
  rating: PropTypes.number.isRequired,
  sets: PropTypes.number.isRequired,
  sets_won: PropTypes.number.isRequired,
  prev_rating: PropTypes.number.isRequired,
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
