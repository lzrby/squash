import React from 'react';
import PropTypes from 'prop-types';

const ARROWS = {
  up: '▲',
  down: '▼',
};

const DeltaArrow = ({ value }) => {
  if (!value) {
    return <span />;
  }
  const type = value > 0 ? 'up' : 'down';
  const arrow = ARROWS[type];
  return (
    <span className={`delta-value__${type}`}>
      {arrow}
      {Math.abs(value)}
    </span>
  );
};

DeltaArrow.propTypes = {
  value: PropTypes.number,
};

export default DeltaArrow;
