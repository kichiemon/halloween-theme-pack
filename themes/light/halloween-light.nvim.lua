-- Halloween Day colorscheme for Neovim
local M = {}

M.colors = {
  bg = "#faf4eb",
  fg = "#241432",
  card = "#f2e7d8",
  secondary = "#e8dcce",
  muted = "#756388",
  border = "#d8c8b4",
  sidebar = "#f4ece1",
  accent = "#bf4904",
  success = "#1b772d",
  destructive = "#b81438",
  cursor = "#bf4904",
  selection = "#e5d0b5",
  blue = "#2b4acb",
  magenta = "#7e22ce",
  cyan = "#0e7490",
  yellow = "#9e6000",
  ansi = {
    black = "#241432", red = "#b81438",
    green = "#1b772d", yellow = "#9e6000",
    blue = "#2b4acb", magenta = "#7e22ce",
    cyan = "#0e7490", white = "#d8ccbc",
  },
  bright = {
    black = "#5c4d6b", red = "#cf2248",
    green = "#228b37", yellow = "#b56f00",
    blue = "#3b5bdb", magenta = "#9333ea",
    cyan = "#0284c7", white = "#241432",
  },
}

function M.setup()
  vim.cmd("hi clear")
  if vim.fn.exists("syntax_on") then vim.cmd("syntax reset") end
  vim.o.background = "light"
  vim.g.colors_name = "halloween-light"
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
