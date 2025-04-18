import { Boot } from './scenes/BootMines.js';
import { Preloader } from './scenes/PreloaderMines.js';
import { Game } from './scenes/GameMines.js';

const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game-container',
    backgroundColor: '#028af8',
    physics: {
        default: 'arcade',
        arcade: {
            debug: false
        }
    },
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    scene: [
        Boot,
        Preloader,
        Game
    ],
    pixelArt: true
};

new Phaser.Game(config);
