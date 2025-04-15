import { Player } from '../../gameObjects/Player.js';

export class Game extends Phaser.Scene {
    constructor() {
        super('Game');

    }

    create() {
        this.add.image(400, 300, 'cave');

        this.coal = this.add.image(400, 300, 'coal');
        
        this.cursors = this.input.keyboard.createCursorKeys();

   }

}