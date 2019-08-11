const RED = 0;
const GREEN = 120;

export const colorByPercent = (percent, start = RED, end = GREEN) => {
  const delta = (end - start) * (percent / 100);
  const hue = start + delta;
  return `hsl(${hue}, 80%, 50%)`;
};
