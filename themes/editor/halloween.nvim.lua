-- Halloween colorscheme for Neovim
local M = {}

M.colors = {
  bg = "#1a0d2e",
  fg = "#f4e7d3",
  card = "#241340",
  secondary = "#2d1b4e",
  muted = "#b8a9d9",
  border = "#3d2a5e",
  sidebar = "#150a24",
  accent = "#ff6b35",
  success = "#39ff14",
  destructive = "#ff4d6d",
  cursor = "#ff6b35",
  selection = "#3d2a5e",
  blue = "#6b8cff",
  magenta = "#c77dff",
  cyan = "#5ffbf1",
  yellow = "#ffb347",
  ansi = {
    black = "#2d1b4e", red = "#ff4d6d",
    green = "#39ff14", yellow = "#ffb347",
    blue = "#6b8cff", magenta = "#c77dff",
    cyan = "#5ffbf1", white = "#f4e7d3",
  },
  bright = {
    black = "#4a3570", red = "#ff7a95",
    green = "#7fff6b", yellow = "#ffd28a",
    blue = "#9db3ff", magenta = "#ddb3ff",
    cyan = "#9dfff7", white = "#fff5e6",
  },
}

function M.setup()
  vim.cmd("hi clear")
  if vim.fn.exists("syntax_on") then vim.cmd("syntax reset") end
  vim.o.background = "dark"
  vim.g.colors_name = "halloween"
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
