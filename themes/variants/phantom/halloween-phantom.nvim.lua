-- Halloween Phantom Mint colorscheme for Neovim
local M = {}

M.colors = {
  bg = "#0e1626",
  fg = "#e6edf5",
  card = "#152033",
  secondary = "#1c2b45",
  muted = "#8fa2b8",
  border = "#273a5a",
  sidebar = "#0a101d",
  accent = "#2ef8a0",
  success = "#48f78b",
  destructive = "#ff5277",
  cursor = "#2ef8a0",
  selection = "#223859",
  blue = "#64b5f6",
  magenta = "#cf8eff",
  cyan = "#2ef8a0",
  yellow = "#ffd166",
  ansi = {
    black = "#1c2b45", red = "#ff5277",
    green = "#48f78b", yellow = "#ffd166",
    blue = "#64b5f6", magenta = "#cf8eff",
    cyan = "#2ef8a0", white = "#e6edf5",
  },
  bright = {
    black = "#344b70", red = "#ff7595",
    green = "#72ffaa", yellow = "#ffe08a",
    blue = "#90caf9", magenta = "#e1b5ff",
    cyan = "#7affce", white = "#ffffff",
  },
}

function M.setup()
  vim.cmd("hi clear")
  if vim.fn.exists("syntax_on") then vim.cmd("syntax reset") end
  vim.o.background = "dark"
  vim.g.colors_name = "halloween-phantom"
  local hi = vim.api.nvim_set_hl
  hi(0, "Normal", { bg = M.colors.bg, fg = M.colors.fg })
  hi(0, "Comment", { fg = M.colors.muted, italic = true })
  hi(0, "Keyword", { fg = M.colors.accent, bold = true })
  hi(0, "String", { fg = M.colors.success })
  hi(0, "Number", { fg = M.colors.destructive })
  hi(0, "Function", { fg = M.colors.blue })
  hi(0, "Type", { fg = M.colors.magenta })
  hi(0, "Operator", { fg = M.colors.cyan })
  hi(0, "Visual", { bg = M.colors.selection })
  hi(0, "Cursor", { bg = M.colors.cursor })
  hi(0, "LineNr", { fg = M.colors.muted })
  hi(0, "CursorLineNr", { fg = M.colors.accent, bold = true })
  hi(0, "StatusLine", { bg = M.colors.secondary, fg = M.colors.fg })
  hi(0, "VertSplit", { fg = M.colors.border })
  hi(0, "Pmenu", { bg = M.colors.card, fg = M.colors.fg })
  hi(0, "PmenuSel", { bg = M.colors.accent, fg = M.colors.bg })
  hi(0, "Search", { bg = M.colors.accent, fg = M.colors.bg })
  hi(0, "IncSearch", { bg = M.colors.success, fg = M.colors.bg })
end

M.setup()
return M
