-- Halloween Cyberpunk colorscheme for Neovim
local M = {}

M.colors = {
  bg = "#0d0221",
  fg = "#fcf7ff",
  card = "#19053b",
  secondary = "#240046",
  muted = "#9d79bc",
  border = "#5a189a",
  sidebar = "#090014",
  accent = "#ff6d00",
  success = "#00f5d4",
  destructive = "#ff0054",
  cursor = "#ff6d00",
  selection = "#3c096c",
  blue = "#7000ff",
  magenta = "#c77dff",
  cyan = "#00f5d4",
  yellow = "#ffee32",
  ansi = {
    black = "#240046", red = "#ff0054",
    green = "#00f5d4", yellow = "#ffee32",
    blue = "#7000ff", magenta = "#c77dff",
    cyan = "#00f5d4", white = "#fcf7ff",
  },
  bright = {
    black = "#5a189a", red = "#ff3377",
    green = "#5cffee", yellow = "#fff275",
    blue = "#9d4edd", magenta = "#e0aaff",
    cyan = "#70fff3", white = "#ffffff",
  },
}

function M.setup()
  vim.cmd("hi clear")
  if vim.fn.exists("syntax_on") then vim.cmd("syntax reset") end
  vim.o.background = "dark"
  vim.g.colors_name = "halloween-cyberpunk"
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
