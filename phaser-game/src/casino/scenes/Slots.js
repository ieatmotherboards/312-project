import { CoinCounter } from '../../gameObjects/CoinCounter.js';

export class Slots extends Phaser.Scene {
    constructor() {
        super('Slots');

    }

    create() {
        this.add.image(400, 300, 'slots_bg').setDisplaySize(800, 600);
    }
}