terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "serverless_api" {
  name     = "rg-serverless-api"
  location = "eastus"
}

resource "azurerm_service_plan" "serverless_api" {
  name                = "plan-serverless-api"
  resource_group_name = azurerm_resource_group.serverless_api.name
  location            = azurerm_resource_group.serverless_api.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "api_handler" {
  name                = "func-serverless-api-handler"
  resource_group_name = azurerm_resource_group.serverless_api.name
  location            = azurerm_resource_group.serverless_api.location
  service_plan_id     = azurerm_service_plan.serverless_api.id

  site_config {}
}

resource "azurerm_api_management" "gateway" {
  name                = "apim-serverless-api"
  resource_group_name = azurerm_resource_group.serverless_api.name
  location            = azurerm_resource_group.serverless_api.location
  publisher_name      = "Patterns"
  publisher_email     = "patterns@example.com"
  sku_name            = "Consumption_0"
}

resource "azurerm_api_management_api" "serverless" {
  name                = "serverless-api"
  resource_group_name = azurerm_resource_group.serverless_api.name
  api_management_name = azurerm_api_management.gateway.name
  revision            = "1"
  display_name        = "Serverless API"
  path                = "api"
  protocols           = ["http"]
}

resource "azurerm_storage_account" "items" {
  name                     = "stserverlessapiitems"
  resource_group_name      = azurerm_resource_group.serverless_api.name
  location                 = azurerm_resource_group.serverless_api.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_table" "items" {
  name                 = "items"
  storage_account_name = azurerm_storage_account.items.name
}
