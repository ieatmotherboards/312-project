import { Boot } from './scenes/BootCasino.js';
import { Game } from './scenes/GameCasino.js';
import { GameOver } from './scenes/GameOver.js';
import { Preloader } from './scenes/PreloaderCasino.js';
import { Slots } from './scenes/Slots.js';
import { CoinFlip } from './scenes/CoinFlip.js';
import { Mines } from './scenes/Mines.js'

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
            // gravity: { y: 500 }
        }
    },
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    scene: [
        Boot,
        Preloader,
        Game,
        GameOver,
        Slots,
        CoinFlip,
        Mines
    ],
    pixelArt: true
};

new Phaser.Game(config);
