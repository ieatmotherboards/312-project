import { Hitbox } from './Hitbox_no_virus.js';

export class SlotMachine extends Phaser.GameObjects.GameObject {

    constructor(scene, x, y, key) {
        super(scene, key);
        // initializes display sprite
        this.sprite = this.scene.physics.add.staticSprite(x, y, key).setScale(2.5, 2.5).refreshBody();
        // collider with player
        this.scene.physics.add.collider(this.sprite, this.scene.player);

        this.interacted = false;
    }

    addOverlapBox(xOff, yOff, scale) {
        this.hitbox = new Hitbox(this.scene, this, this.sprite.x + xOff, this.sprite.y + yOff, scale);
        this.hitbox.addOverlap(this.scene.player);
    }

    startOverlap() {
        this.scene.slotOverlaps.add(this);
        this.scene.playPopupVisible(true);
    }

    duringOverlap() {
        if (this.scene.keySpace.isDown && !this.interacted && !this.scene.disableMovement) {
            this.interacted = true;
            this.scene.slotsSwap();
        }
        else if (!this.scene.keySpace.isDown && this.interacted) {
            this.interacted = false;
        }
    }

    stopOverlap() {
        this.scene.slotOverlaps.delete(this);
        this.scene.stoppedColliding();
    }
}