-- lua/plugins/treesitter.lua



return {

  "nvim-treesitter/nvim-treesitter",

  build = ":TSUpdate",

  config = function()

    local config = require("nvim-treesitter.configs")

    config.setup({

      ensure_installed = { "c", "lua", "vim", "vimdoc", "python" },

      sync_install = false,

      highlight = { enable = true },

      indent = { enable = true },

    })

  end

}

