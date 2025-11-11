provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "my-resources"
  location = "East US"
}
