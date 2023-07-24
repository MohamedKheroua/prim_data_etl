<h2 align="center">Procédure d'installation de l'outil VcXsrv</h2>

<br />

### **À propos**

On pourra suivre cette procédure pour installer et paramétrer VcXsrv avant de lancer les scripts permettant de récupérer les données depuis l'API PRIM.

<br />

### **Configuration de l'environnement de travail**

Les instructions suivantes permettent de configurer l'environnement de travail pour le lancement automatisé de Chrome sur sa machine.

### Pré-requis

- Python 3

- {Visual Studio Code + distribution WSL2} ou Linux

### Installation (pour configuration Windows + WSL2)

1. Installer Chrome
    
    Il faut installer Chrome et ses dépendances sur WSL2 même s'il est déjà installé côté Windows

    - les dépendances de Chrome nécessaire :

        ```
        sudo apt-get update
        sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4
        ```

    - Chrome

        ```
        sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo apt install ./google-chrome-stable_current_amd64.deb
        ```

    <br/>

    Vérifier que l'installation a fonctionné :

    ```
    google-chrome --version
    ```

    <br/>

    Le fichier d'installation de Chrome peut être supprimé du répertoire une fois l'installation terminée :

    ```
    sudo rm google-chrome-stable_current_amd64.deb
    ```

<br/>

2. Installer ChromeDriver

    Il faut télécharger <a href="https://chromedriver.chromium.org/downloads">ici</a> la version de ChromeDriver associée à la version de Google Chrome installée précédemment.
    
    *Par exemple, `chromedriver_linux64.zip` pour la version `110.0.5481.177` de Google Chrome*

    Puis :

    ```
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver
    ```

    <br/>

    Vérifier que l'installation a fonctionné :

    ```
    chromedriver --version
    ```

    <br/>

    Si chromeDriver est aussi installé côté Windows, vérifier que dans WSL2, il pointe vers la bonne version (normalement vers /usr/bin/chromedriver) : :

    ```
    which chromedriver
    ```

<br/>

3. Installer VcXsrv

    Pour pouvoir lancer Chrome depuis WSL2, une application permettant de simuler une sortie écran est nécessaire, par exemple <a href="https://sourceforge.net/projects/vcxsrv/">VcXsrv</a>.

    Installer VcXsrv sur Windows.

<br/>

4. Paramétrer la variable d'environnement `DISPLAY`

    Dans WSL2, la variable d'environnement `DISPLAY` permettra à VcXsrv de savoir quelle adresse IP utiliser. Il faut donc paramétrer cette variable avant de pouvoir lancer VcXsrv :

    ```
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0
    ```

    *Cette ligne de commande pourra être copiée dans le fichier `.bashrc` (ou autre fichier équivalent) pour être prise en compte automatiquement à chaque lancement de WSL2.*

    <br/>

    La variable d'environnement `DISPLAY` doit maintenant afficher une adresse IP du type `172.X.X.X:0.0` :
    
    ```
    echo $DISPLAY
    ```

<br/>

5. Lancer xlaunch.exe depuis le dossier d'installation de VcXsrv

    Les options par défaut peuvent être laissées, en vérifiant que l'option "Disable access control" est bien cochée.

<br/>

5. Lancement de Google Chrome

    En lançant la commande :

    ```
    google-chrome
    ```

    une fenêtre du navigateur Chrome devrait apparaître. Si tel est le cas, le lancement automatique de Google Chrome (par exemple en utilisant la bibliothèque Selenium de Python) devrait également fonctionner.

<br/>

### Sources

https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/