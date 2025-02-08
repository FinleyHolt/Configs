return {

  -- Mason plugin

  {

    "williamboman/mason.nvim",

    config = function()

      require("mason").setup()

    end,

  },



  -- Mason LSPconfig plugin (to integrate Mason with LSPconfig)

  {

    "williamboman/mason-lspconfig.nvim",

    config = function()

      require("mason-lspconfig").setup({

        ensure_installed = { "pyright", "ruff", "pylsp" }, -- Install Python tools: Pyright, Ruff, pylsp

      })

    end,

  },



  -- Python LSP Config (Pyright and pylsp setup)

  {

    "neovim/nvim-lspconfig",

    config = function()

      local lspconfig = require("lspconfig")



      -- Pyright setup for Python

      lspconfig.pyright.setup({})



      -- Pylsp setup for Python (if you prefer another LSP server)

      lspconfig.pylsp.setup({

        settings = {

          pylsp = {

            plugins = {

              autopep8 = { enabled = true },  -- Enable autopep8 plugin for pylsp

              pyflakes = { enabled = true },

              pycodestyle = { enabled = true },

            },

          },

        },

      })

    end

  },



  -- Mason Debug Adapter Protocol (DAP) setup for Python

  {

    "mfussenegger/nvim-dap",

    config = function()

      local dap = require("dap")



      -- Python Debug Adapter (using debugpy)

      dap.adapters.python = {

        type = "executable",

        command = "python",

        args = { "-m", "debugpy.adapter" },

      }



      dap.configurations.python = {

        {

          type = "python",

          request = "launch",

          name = "Launch file",

          program = "${file}",

        },

      }

    end

  },



  -- Neotest integration for Python testing

  {

    "nvim-neotest/neotest",

    dependencies = {

      "nvim-lua/plenary.nvim",

      "nvim-telescope/telescope.nvim",

      "nvim-neotest/nvim-nio", -- Add this dependency for neotest

      "nvim-neotest/neotest-python", -- Install the neotest-python adapter

    },

    config = function()

      require("neotest").setup({

        adapters = {

          require("neotest-python")({

            dap = { justMyCode = false },

          }),

        },

      })

    end

  },



  -- Install and configure Python-related tools with Mason

  {

    "williamboman/mason.nvim",

    config = function()

      require("mason").setup({

        ensure_installed = { "pyright", "ruff", "black", "pylsp", "debugpy" },

      })

    end

  },

}

