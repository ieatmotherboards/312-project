import { Boot } from './scenes/BootRoulette.js';
import { Roulette } from './scenes/Roulette.js';
import { Preloader } from './scenes/PreloaderRoulette.js';

const config = {
    type: Phaser.AUTO,
    width: window.innerWidth,
    height: window.innerHeight,
    scale: {
        mode: Phaser.Scale.RESIZE,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: '100%',
        height: '100%',
    },
    backgroundColor: '#1a1a1a',
    parent: 'game-container',
    scene: [
        Boot,
        Preloader,
        Roulette
        ]
};

new Phaser.Game(config);