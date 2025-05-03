import { Hitbox } from './Hitbox_no_virus.js';

export class MineEntrance extends Phaser.GameObjects.Sprite {

    constructor(scene, x, y) {
        super(scene, x, y, 'mine_entrance');
        this.setScale(3, 3);
        this.scene.add.existing(this);

        this.hitbox = new Hitbox(this.scene, this, x + 60, y, 10);
        this.hitbox.addOverlap(this.scene.player);
    }

    startOverlap() {
        this.scene.minesSwap();
    }

    duringOverlap() {
        
    }

    stopOverlap() {
        
    }
}