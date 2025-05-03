import { Boot } from './scenes/BootRoulette.js';
import { Roulette } from './scenes/Roulette.js';
import { Preloader } from './scenes/PreloaderRoulette.js';

const config = {
    type: Phaser.AUTO,
    width: 1920,
    height: 955,
    parent: 'game-container',
    backgroundColor: '#1a1a1a',
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    scene: [
        Boot,
        Preloader,
        Roulette
        ],
    pixelArt: true
};

new Phaser.Game(config);