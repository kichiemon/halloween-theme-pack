-- Halloween Vampire Velvet colorscheme for Neovim
local M = {}

M.colors = {
  bg = "#4a0e17",
  fg = "#f7ebdc",
  card = "#380a11",
  secondary = "#5a131f",
  muted = "#bfa3a8",
  border = "#6a1b28",
  sidebar = "#2d070d",
  accent = "#d4af37",
  success = "#2ebd6e",
  destructive = "#ff4d6d",
  cursor = "#d4af37",
  selection = "#631724",
  blue = "#6ba3ff",
  magenta = "#d47ae8",
  cyan = "#45dfdf",
  yellow = "#e5b842",
  ansi = {
    black = "#380a11", red = "#ff4d6d",
    green = "#2ebd6e", yellow = "#e5b842",
    blue = "#6ba3ff", magenta = "#d47ae8",
    cyan = "#45dfdf", white = "#f7ebdc",
  },
  bright = {
    black = "#6a1b28", red = "#ff758f",
    green = "#52e896", yellow = "#ffd166",
    blue = "#9bc4ff", magenta = "#ebb2f7",
    cyan = "#82f7f7", white = "#ffffff",
  },
}

function M.setup()
  vim.cmd("hi clear")
  if vim.fn.exists("syntax_on") then vim.cmd("syntax reset") end
  vim.o.background = "dark"
  vim.g.colors_name = "halloween-vampire"
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
