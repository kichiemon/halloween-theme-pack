// Halloween OLED theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#000000',
    foregroundColor: '#f4e7d3',
    borderColor: '#2c1845',
    cursorColor: '#ff6b35',
    cursorAccentColor: '#000000',
    selectionColor: 'rgba(44, 24, 69, 0.5)',
    colors: {
      black: '#1a0a2a',
      red: '#ff4d6d',
      green: '#39ff14',
      yellow: '#ffb347',
      blue: '#6b8cff',
      magenta: '#c77dff',
      cyan: '#5ffbf1',
      white: '#f4e7d3',
      lightBlack: '#3b1e5c',
      lightRed: '#ff7a95',
      lightGreen: '#7fff6b',
      lightYellow: '#ffd28a',
      lightBlue: '#9db3ff',
      lightMagenta: '#ddb3ff',
      lightCyan: '#9dfff7',
      lightWhite: '#ffffff',
    },
  });
};
