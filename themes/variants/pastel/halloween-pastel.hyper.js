// Halloween Pastel theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#faf5fc',
    foregroundColor: '#3c2a4d',
    borderColor: '#dcc9e8',
    cursorColor: '#bf4904',
    cursorAccentColor: '#faf5fc',
    selectionColor: 'rgba(229, 208, 240, 0.5)',
    colors: {
      black: '#3c2a4d',
      red: '#b81438',
      green: '#1b772d',
      yellow: '#9e6000',
      blue: '#2b4acb',
      magenta: '#8b3da8',
      cyan: '#0e7490',
      white: '#dcc9e8',
      lightBlack: '#674f78',
      lightRed: '#cf2248',
      lightGreen: '#228b37',
      lightYellow: '#b56f00',
      lightBlue: '#3b5bdb',
      lightMagenta: '#a855f7',
      lightCyan: '#0284c7',
      lightWhite: '#3c2a4d',
    },
  });
};
