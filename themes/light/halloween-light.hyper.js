// Halloween Day theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#faf4eb',
    foregroundColor: '#241432',
    borderColor: '#d8c8b4',
    cursorColor: '#bf4904',
    cursorAccentColor: '#faf4eb',
    selectionColor: 'rgba(229, 208, 181, 0.5)',
    colors: {
      black: '#241432',
      red: '#b81438',
      green: '#1b772d',
      yellow: '#9e6000',
      blue: '#2b4acb',
      magenta: '#7e22ce',
      cyan: '#0e7490',
      white: '#d8ccbc',
      lightBlack: '#5c4d6b',
      lightRed: '#cf2248',
      lightGreen: '#228b37',
      lightYellow: '#b56f00',
      lightBlue: '#3b5bdb',
      lightMagenta: '#9333ea',
      lightCyan: '#0284c7',
      lightWhite: '#241432',
    },
  });
};
