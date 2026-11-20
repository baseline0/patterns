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

resource "azurerm_resource_group" "event_driven" {
  name     = "rg-event-driven"
  location = "eastus"
}

resource "azurerm_service_plan" "event_driven" {
  name                = "plan-event-driven"
  resource_group_name = azurerm_resource_group.event_driven.name
  location            = azurerm_resource_group.event_driven.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "consumer" {
  name                = "func-event-driven-consumer"
  resource_group_name = azurerm_resource_group.event_driven.name
  location            = azurerm_resource_group.event_driven.location
  service_plan_id     = azurerm_service_plan.event_driven.id

  site_config {}
}

resource "azurerm_storage_account" "events" {
  name                     = "steventdrivenevents"
  resource_group_name      = azurerm_resource_group.event_driven.name
  location                 = azurerm_resource_group.event_driven.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_queue" "events" {
  name                 = "events"
  storage_account_name = azurerm_storage_account.events.name
}

resource "azurerm_storage_queue" "events_dead_letter" {
  name                 = "events-dead-letter"
  storage_account_name = azurerm_storage_account.events.name
}

resource "azurerm_storage_table" "processed_events" {
  name                 = "processedevent"
  storage_account_name = azurerm_storage_account.events.name
}
