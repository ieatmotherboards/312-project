import { Hitbox } from './Hitbox_no_virus.js';

export class RouletteTable extends Phaser.Physics.Arcade.Sprite {

    constructor(scene, x, y) {
        super(scene, x, y, 'roulette_table');
        // this.setScale(3);
        this.scene.add.existing(this);
        this.scene.physics.add.existing(this);
        // collider with player
        this.scene.physics.add.collider(this, this.scene.player);

        this.hitbox = new Hitbox(this.scene, this, x, y, 6);
        this.hitbox.addOverlap(this.scene.player);

        this.interacted = false;
    }

    startOverlap() {
        this.scene.gameOverlaps.add(this);
        this.scene.playPopupVisible(true);
    }

    duringOverlap() {
        if (this.scene.keySpace.isDown && !this.interacted && !this.scene.disableMovement) {
            this.interacted = true;
            this.scene.rouletteSwap();
        }
        else if (!this.scene.keySpace.isDown && this.interacted) {
            this.interacted = false;
        }
    }

    stopOverlap() {
        this.scene.gameOverlaps.delete(this);
        this.scene.stoppedColliding();
    }
}