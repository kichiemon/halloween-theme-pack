// Halloween Cyberpunk theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#0d0221',
    foregroundColor: '#fcf7ff',
    borderColor: '#5a189a',
    cursorColor: '#ff6d00',
    cursorAccentColor: '#0d0221',
    selectionColor: 'rgba(60, 9, 108, 0.5)',
    colors: {
      black: '#240046',
      red: '#ff0054',
      green: '#00f5d4',
      yellow: '#ffee32',
      blue: '#7000ff',
      magenta: '#c77dff',
      cyan: '#00f5d4',
      white: '#fcf7ff',
      lightBlack: '#5a189a',
      lightRed: '#ff3377',
      lightGreen: '#5cffee',
      lightYellow: '#fff275',
      lightBlue: '#9d4edd',
      lightMagenta: '#e0aaff',
      lightCyan: '#70fff3',
      lightWhite: '#ffffff',
    },
  });
};
