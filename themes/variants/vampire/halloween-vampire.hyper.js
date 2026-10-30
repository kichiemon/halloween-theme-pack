// Halloween Vampire Velvet theme for Hyper
exports.decorateConfig = (config) => {
  return Object.assign({}, config, {
    backgroundColor: '#4a0e17',
    foregroundColor: '#f7ebdc',
    borderColor: '#6a1b28',
    cursorColor: '#d4af37',
    cursorAccentColor: '#4a0e17',
    selectionColor: 'rgba(99, 23, 36, 0.5)',
    colors: {
      black: '#380a11',
      red: '#ff4d6d',
      green: '#2ebd6e',
      yellow: '#e5b842',
      blue: '#6ba3ff',
      magenta: '#d47ae8',
      cyan: '#45dfdf',
      white: '#f7ebdc',
      lightBlack: '#6a1b28',
      lightRed: '#ff758f',
      lightGreen: '#52e896',
      lightYellow: '#ffd166',
      lightBlue: '#9bc4ff',
      lightMagenta: '#ebb2f7',
      lightCyan: '#82f7f7',
      lightWhite: '#ffffff',
    },
  });
};
