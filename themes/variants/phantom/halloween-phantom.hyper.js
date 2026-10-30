// Halloween Phantom Mint theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#0e1626',
    foregroundColor: '#e6edf5',
    borderColor: '#273a5a',
    cursorColor: '#2ef8a0',
    cursorAccentColor: '#0e1626',
    selectionColor: 'rgba(34, 56, 89, 0.5)',
    colors: {
      black: '#1c2b45',
      red: '#ff5277',
      green: '#48f78b',
      yellow: '#ffd166',
      blue: '#64b5f6',
      magenta: '#cf8eff',
      cyan: '#2ef8a0',
      white: '#e6edf5',
      lightBlack: '#344b70',
      lightRed: '#ff7595',
      lightGreen: '#72ffaa',
      lightYellow: '#ffe08a',
      lightBlue: '#90caf9',
      lightMagenta: '#e1b5ff',
      lightCyan: '#7affce',
      lightWhite: '#ffffff',
    },
  });
};
