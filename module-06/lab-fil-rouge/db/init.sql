-- init.sql — Initialisation de la base de données IT-Support Portal
-- Ce script est exécuté automatiquement au premier démarrage de PostgreSQL

-- Table des connexions (journal d'accès)
CREATE TABLE IF NOT EXISTS access_log (
    id          SERIAL PRIMARY KEY,
    ip_address  VARCHAR(50),
    page        VARCHAR(200),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des services IT surveillés
CREATE TABLE IF NOT EXISTS services (
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(100) NOT NULL,
    description TEXT,
    statut      VARCHAR(20) DEFAULT 'actif',
    icone       VARCHAR(10) DEFAULT '⚙️',
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Données initiales : liste des services IT
INSERT INTO services (nom, description, statut, icone) VALUES
    ('Serveur Web',             'Serveur Apache/Nginx principal', 'actif',   '🌐'),
    ('Base de données',         'Serveur PostgreSQL',             'actif',   '🗄️'),
    ('Serveur de fichiers (NAS)', 'Stockage réseau partagé',      'actif',   '💾'),
    ('VPN',                     'Accès distant sécurisé',         'inactif', '🔒'),
    ('Serveur de sauvegardes',  'Sauvegarde quotidienne 3h',      'actif',   '📦'),
    ('Imprimantes réseau',      'Imprimantes salles A et B',      'actif',   '🖨️');
