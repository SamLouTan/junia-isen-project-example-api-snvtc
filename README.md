# Shop App API on Azure Cloud

Ce projet démontre une application simple déployée sur Azure à l'aide de Terraform. Les étudiants peuvent forker ce dépôt pour compléter leurs devoirs.

## Membres du groupe

- **Dussaussois Victor**
- **Contini Nicolas**
- **Bouhelassa Samy**
- **Boulnois Constant**
- **Delaporte Théo**

## Project Structure

- `api/`: Contient le code de l'API Flask.
- `infrastructure/`: Contient le code Terraform pour provisionner l'infrastructure Azure.
- `.github/`: Contient les workflows GitHub Actions pour le CI/CD.

## Getting Started

### Prérequis
- Python 3.9 ou version ultérieure
- Terraform 1.5 ou version ultérieure
- Compte Azure

### Déployer l'Infrastructure avec Terraform
1. **Configurer des variables Terraform** :
   - **`subscription_id`** : Identifiant du compte Azure
   - **`location`** : serveur pour héberger la ressource
   - **`username_db`** : usernae de la vase de données
   - **`password_db`** : mot de passe de la base de données
   - **`docker_image_name`** : chemin de la l'image docker
   - **`docker_registry_username`** : identifiant pour l'image docker
   - **`docker_registry_password`** : tocken github pour l'image docker

   Il est possible de déclarer ces variables dans un fichier `terraform.tfvars` ou elles seront demandé lors des commandes de déploiement

2. **Déployer l'infrastructure** :
   
      Saisir les commandes suivantes dans un termainal au niveau du `main.tf`
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

### CI/CD

   À chaque fois qu'un commit est fait, les workflows suivants sont exécutés :
1. **Tests**
   - Test sur l'API
   - Test sur le terraform
3. **Déploiment de l'image docker** :
   - Ajouter en secret du repo le tocken de github pour l'utiliser comme mot de passe
   - Build de l'image Docker à partir du Dockerfile situé dans `api/`.
   - Pousser l'image vers le registre `ghcr` avec les informations d'authentification appropriées.
   - Mise à jour de l'application Azure avec la nouvelle image.

### API

- `\`: acceuil de l'API
- `\items` : Permet de voir tous les items du shop
- `\baskets` : Permet de voir le panier des clients
-  `\users` : Permet de voir tous les utilisateurs

   