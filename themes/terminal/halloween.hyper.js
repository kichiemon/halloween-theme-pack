// Halloween theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#1a0d2e',
    foregroundColor: '#f4e7d3',
    borderColor: '#3d2a5e',
    cursorColor: '#ff6b35',
    cursorAccentColor: '#1a0d2e',
    selectionColor: 'rgba(61, 42, 94, 0.5)',
    colors: {
      black: '#2d1b4e',
      red: '#ff4d6d',
      green: '#39ff14',
      yellow: '#ffb347',
      blue: '#6b8cff',
      magenta: '#c77dff',
      cyan: '#5ffbf1',
      white: '#f4e7d3',
      lightBlack: '#4a3570',
      lightRed: '#ff7a95',
      lightGreen: '#7fff6b',
      lightYellow: '#ffd28a',
      lightBlue: '#9db3ff',
      lightMagenta: '#ddb3ff',
      lightCyan: '#9dfff7',
      lightWhite: '#fff5e6',
    },
  });
};
