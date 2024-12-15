provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}


resource "random_id" "random" {
  byte_length = 6
}

resource "azurerm_resource_group" "shop" {
  name     = "shop-app-rg-${random_id.random.hex}"
  location = var.location
}

module "vnet" {
  source                = "./modules/vnet"
  resource_group_name   = azurerm_resource_group.shop.name
  location              = var.location
  random_id             = random_id.random.hex
  subnet_id_app_service = module.vnet.subnet_id_app_service
  subnet_id_db          = module.vnet.subnet_id_db
}

module "database" {
  source              = "./modules/bdd"
  resource_group_name = azurerm_resource_group.shop.name
  location            = var.location
  username_db         = var.username_db
  password_db         = var.password_db
  random_id           = random_id.random.hex
  vnet_id             = module.vnet.vnet_id
  subnet_id_db        = module.vnet.subnet_id_db
}

module "gateway" {
  source                = "./modules/gateway"
  resource_group_name   = azurerm_resource_group.shop.name
  location              = var.location
  random_id             = random_id.random.hex
  subnet_id_app_gateway = module.vnet.subnet_id_app_gateway
  app_service_host      = module.app_service.app_service_host
}

module "app_service" {
  source                   = "./modules/app_service"
  resource_group_name      = azurerm_resource_group.shop.name
  random_id                = random_id.random.hex
  location                 = var.location
  database_host            = module.database.database_host
  username_db              = var.username_db
  password_db              = var.password_db
  database_name            = module.database.database_name
  subnet_id_app_service    = module.vnet.subnet_id_app_service
  docker_image_name        = var.docker_image_name
  docker_registry_username = var.docker_registry_username
  docker_registry_password = var.docker_registry_password
}